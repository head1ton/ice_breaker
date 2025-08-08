from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
# from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from agent.linkedin_lookup_agent import lookup as linkedin_look_agent
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_look_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username)

    summary_template = """
            given the information {information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
        """

    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                             template=summary_template)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    print("Ice Breaker Enter")

    ice_break_with(name="Daehwan Cho")
