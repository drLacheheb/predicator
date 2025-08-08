import os
from google import genai
from google.genai import types


class ExamJSONBuilder:
    def __init__(self, api_key=None, model="gemini-2.5-flash-lite"):
        self.api_key = api_key or os.getenv("API_KEY")
        self.model = model
        self.client = self.__create_client()

    def __create_client(self):
        return genai.Client(api_key=self.api_key)

    def __prepare_contents(self, pdf_b64):
        return [
            types.Content(
                role="user",
                parts=[types.Part.from_bytes(mime_type="application/pdf", data=pdf_b64)],
            ),
        ]

    def __generate_config(self):
        return types.GenerateContentConfig(
            temperature=0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                description="A flexible schema to structure exams with objective and subjective questions",
                required=["exam"],
                properties={
                    "exam": genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["title", "questions"],
                        properties={
                            "title": genai.types.Schema(type=genai.types.Type.STRING),
                            "institution": genai.types.Schema(type=genai.types.Type.STRING),
                            "date": genai.types.Schema(type=genai.types.Type.STRING),
                            "duration": genai.types.Schema(type=genai.types.Type.STRING),
                            "total_questions": genai.types.Schema(type=genai.types.Type.INTEGER),
                            "instructions": genai.types.Schema(type=genai.types.Type.STRING),
                            "questions": genai.types.Schema(
                                type=genai.types.Type.ARRAY,
                                items=genai.types.Schema(
                                    type=genai.types.Type.OBJECT,
                                    required=["id", "category", "question_type", "text"],
                                    properties={
                                        "id": genai.types.Schema(type=genai.types.Type.INTEGER),
                                        "category": genai.types.Schema(
                                            type=genai.types.Type.STRING,
                                            enum=["objective", "subjective"],
                                        ),
                                        "question_type": genai.types.Schema(
                                            type=genai.types.Type.STRING,
                                            enum=[
                                                "multiple_choice",
                                                "true_false",
                                                "matching",
                                                "fill_in_the_blank",
                                                "short_answer",
                                                "essay",
                                                "open_ended",
                                                "computational",
                                                "case_study",
                                            ],
                                        ),
                                        "context": genai.types.Schema(type=genai.types.Type.STRING),
                                        "text": genai.types.Schema(type=genai.types.Type.STRING),
                                        "options": genai.types.Schema(
                                            type=genai.types.Type.ARRAY,
                                            items=genai.types.Schema(
                                                type=genai.types.Type.OBJECT,
                                                required=["label", "text"],
                                                properties={
                                                    "label": genai.types.Schema(type=genai.types.Type.STRING),
                                                    "text": genai.types.Schema(type=genai.types.Type.STRING),
                                                },
                                            ),
                                        ),
                                        "answer": genai.types.Schema(
                                            type=genai.types.Type.STRING,
                                            description="Can be a string, an array of strings, or a detailed solution object for subjective questions",
                                        ),
                                        "explanation": genai.types.Schema(type=genai.types.Type.STRING),
                                        "points": genai.types.Schema(type=genai.types.Type.NUMBER),
                                    },
                                ),
                            ),
                        },
                    ),
                },
            ),
            system_instruction=[
                types.Part.from_text(
                    text="You are an AI specialized in structuring exams into a standardized JSON format."
                ),
            ],
        )

    def __stream_and_print(self, contents, config):
        for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
        ):
            print(chunk.text, end="")

    def execute(self, pdf_b64):
        contents = self.__prepare_contents(pdf_b64)
        config = self.__generate_config()
        self.__stream_and_print(contents, config)
