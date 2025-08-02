from pydantic import BaseModel, Field
from agents import Agent

searches = 7

Instructions = f"You are a research planner. You will be given a query and it is your job to return a set of web searches that will best be suited\
    to write a research paper for the given query. Return only the most relevant and important web searches. Output {searches} terms to query for."

class WebSearchItem(BaseModel):
    reason: str=Field(description="Your reasoning for why this search is importatnt to the query.")
    query: str=Field(description="The search term to use for the web search. ")

class WebPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to best answer the query.")

Planner_Agent = Agent(
    name="PlannerAgent",
    instructions=Instructions,
    model="gpt-4o-mini",
    output_type=WebPlan,
)

