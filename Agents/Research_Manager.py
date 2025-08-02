from agents import Agent,Runner,trace,gen_trace_id
from Search_Agent import Search_Agent
from Planner_Agent import Planner_Agent,WebSearchItem,WebPlan
from Writer_Agent import Writer_Agent, ReportData
import asyncio

class ResearchManager:

    async def run(self,query: str):
        trace_id=gen_trace_id()
        with trace("Ananya research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Research complete!!!"
            yield report.markdown_report
    
    async def plan_searches(self,query: str) -> WebPlan:
        print("Planning searches...")
        result = await Runner.run(
            Planner_Agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebPlan)
    
    async def perform_searches(self, search_plan: WebPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results
    
    async def search(self,item: WebSearchItem) ->str | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason} "
        try:
            result = await Runner.run(
                Search_Agent,
                input
            )
            return str(result.final_output)
        except Exception:
            return None
    
    async def write_report(self,query:str, search_results: list[str]) -> ReportData:
        print("Thinking about report..")
        input=f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            Writer_Agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    