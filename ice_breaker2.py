from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties2.twitter2 import scrape_user_tweets
from third_parties2.linkedin2 import scrape_linkedin_profile
from agents2.linkedin_lookup_agent2 import lookup
from agents2.twitter_lookup_agent import lookup as twitter_lookup

def ice_breaker_with(name: str) -> str:
    linkedin_user_URL = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_user_URL, mock= True)
    
    twitter_username = twitter_lookup(name=name)
    tweets = scrape_user_tweets(username=twitter_username,mock=True)
    
    summary_template = """
        given the Linkedin information {information} about a person and
        twitter posts {tweets} I want you to create:
        1. a short summary
        2. two interesting facts about them
        
        Use both information from twitter and Linkedin
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "tweets"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    #llm = ChatOllama(model="mistral", temperature=0)
    
    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data, "tweets": tweets})

    print(res)

if __name__ == "__main__":
    load_dotenv(override=True)
    print("Ice Breaker Enter")
    
    ice_breaker_with(name="Denisse Dix Cadeño")
    


