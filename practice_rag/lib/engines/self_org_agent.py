import operator
from typing import Annotated, List, TypedDict, Union
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 1. 状態（State）の定義
class AgentState(TypedDict):
    # メッセージの履歴を逐次的に蓄積
    messages: Annotated[List[BaseMessage], operator.add]
    # 次にどのステップ（役割）が必要かをエージェント自身が判断した結果
    next_action: str

# 2. 自律型エージェントの定義
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def self_organizing_agent(state: AgentState):
    """
    固定された役割を持たず、現在のメッセージ履歴から
    「次に必要な行動（検索、分析、回答）」を自律的に選択して実行する
    """
    messages = state["messages"]
    
    # 論文の知見：役割を固定せず、プロンプトで「次に最適な行動を自律的に選べ」と指示
    system_prompt = (
        "あなたは自己組織化エージェントチームの一員です。"
        "固定された役割はありません。現在のコンテキストを確認し、"
        "不足している情報があれば検索(tool_use)を、"
        "情報が揃っていれば最終回答を作成してください。"
    )
    
    # 最新のメッセージ履歴をLLMに渡し、次のアクションを決定
    response = llm.invoke([HumanMessage(content=system_prompt)] + messages)
    
    # 簡易的なロジックで次の遷移先を判定（実際にはTool Calling等を利用）
    if "FINAL ANSWER" in response.content:
        return {"messages": [response], "next_action": "end"}
    else:
        return {"messages": [response], "next_action": "continue"}

# 3. グラフの構築 (Sequential Protocolの再現)
workflow = StateGraph(AgentState)

# エージェントノードを追加
# 論文の「Sequential」プロトコルに従い、同じノード定義を循環させることで、
# 異なるインスタンスが逐次的に状態を更新していく構造にします
workflow.add_node("agent_v1", self_organizing_agent)
workflow.add_node("agent_v2", self_organizing_agent)

workflow.set_entry_point("agent_v1")

# 自律的な判断に基づく遷移
workflow.add_conditional_edges(
    "agent_v1",
    lambda x: x["next_action"],
    {
        "continue": "agent_v2",
        "end": END
    }
)

workflow.add_conditional_edges(
    "agent_v2",
    lambda x: x["next_action"],
    {
        "continue": "agent_v1",  # 必要に応じてループ
        "end": END
    }
)

app = workflow.compile()