import httpx
from string import Template as StdStringTemplate

from openai import OpenAI, APIError

from .html_interact import extract_essay_body
from .utils import AuthorEssayKV, create_logger, AIRequestError

logger = create_logger(__name__)


def make_ai_prompt(
    prompt: str,
    ai_client: OpenAI,
    model_name: str,
    system_message: str,
) -> str:
    """
    Return the output of the prompt as a string
    """

    if len(prompt) == 0:
        raise AIRequestError("Prompt to an AI Model needs contain words")

    try:
        response = ai_client.chat.completions.create(
            model=model_name,
            n=1,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
    except APIError as error:
        raise AIRequestError(f"Request to {model_name} returned with error: {error}")

    logger.info(f"Request made to '{model_name}' with prompt '{prompt}'")

    return response.choices[0].message.content


AUTHOR_PROMPT: StdStringTemplate = StdStringTemplate("""
You are an admissions officer. From the HTML page below, describe the writer of the article in a single paragraph. Focus on what would be relevant to the admission, describe as though you were the writer e.g I am Qwen, do not be conversational in your response

$html_page
""")  # $html_page is a placeholder

ESSAY_PROMPT: StdStringTemplate = StdStringTemplate("""
You are an admissions officer. For each essay in the page give the essay included. For example

Essay 1
.....essay.....

Essay 2
......essay........

Do not include any conversational text in your response. Include the actual essay in the text and the essay numbering

$html_page
""")


def ai_essay_summarize(body: str) -> AuthorEssayKV:
    """ """

    substitute_object = {"html_page": body}
    author_prompt = AUTHOR_PROMPT.substitute(substitute_object)
    essay_prompt = ESSAY_PROMPT.substitute(substitute_object)

    author_details = make_ai_prompt(author_prompt)
    author_essay = make_ai_prompt(essay_prompt)

    return AuthorEssayKV(author_profile=author_details, author_essay=author_essay)


def extract_essays_from_urls(
    valid_urls: list[str], client: httpx.Client
) -> list[AuthorEssayKV]:
    essays: list[AuthorEssayKV] = list()

    invalid_urls = list()

    for link in valid_urls:
        logger.info(f"Querying {link}")

        try:
            html_body: str = extract_essay_body(client, link)

            author_essay_kv: AuthorEssayKV = ai_essay_summarize(html_body)

            essays.append(author_essay_kv)

            logger.info("processed link:", link)

        except httpx.RequestError as error:
            invalid_urls.append(link)
            logger.fatal(f"Error processing URL {link}: {error}")

        except AIRequestError as error:
            invalid_urls.append(link)
            logger.fatal(f"Error processing URL {link}: {error}")

    if len(invalid_urls) > 0:
        logger.fatal(
            f"Invalid URLs are:\n{'\n'.join([f'{str(i + 1)}. {invalid_urls[i]}' for i in range(len(invalid_urls))])}"
        )

    return essays
