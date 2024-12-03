#!/usr/bin/env python
!pip install --no-cache-dir --no-dependencies --disable-pip-version-check -r requirements.txt

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_community.llms import VLLMOpenAI

# LLM Inference Server URL
inference_server_url = "http://granite-7b-instruct-predictor.ic-shared-llm.svc.cluster.local:8080"

# LLM definition
llm = VLLMOpenAI(           # We are using the vLLM OpenAI-compatible API client. But the Model is running on OpenShift AI, not OpenAI.
    openai_api_key="EMPTY",   # And that is why we don't need an OpenAI key for this.
    openai_api_base= f"{inference_server_url}/v1",
    model_name="granite-7b-instruct",
    top_p=0.92,
    temperature=0.01,
    max_tokens=512,
    presence_penalty=1.03,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

template="""<|system|>
You will be asked a question, to which you need to give an answer.
The answer should not include harmful or illegal content.
If you don't know the answer to a question, answer "I don't know".

<|user|>
### QUESTION:
{input}

### ANSWER:
<|assistant|>
"""
prompt = PromptTemplate(input_variables=["input"], template=template)

conversation = prompt | llm
query = "What is the capital of France?"
conversation.invoke(input=query);
