from pydantic import BaseModel,Field
from agents import Agent 

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)

class ReportData(BaseModel):
    short_summary: str=Field(description="A detailed brief on the findings.")

    markdown_report: str=Field(description="The final report")

    conclusion: str=Field(description="The final conclusion of the report")
    follow_up_questions: list[str]=Field(description="Suggested topics to research further")

Writer_Agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)

