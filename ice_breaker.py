from typing import Tuple

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
# from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from agent.linkedin_lookup_agent import lookup as linkedin_look_agent
from agent.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parser import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets_mock

load_dotenv()


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_look_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets_mock(username=twitter_username)

    summary_template = """
            given the information about a person from linkedin {information},
             and twitter posts {twitter_posts} I want you to create:
            1. a short summary
            2. two interesting facts about them
            
            Use both information from twitter and Linkedin
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    print("Ice Breaker Enter")

    ice_break_with(name="Daehwan Cho")
