import chainlit as cl

from src.ingestion import load_and_split_document
import src.vectorstore as vs
from src.agent import ask_agent

ACCEPTED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
]


def upload_action():
    return cl.Action(name="upload_more", payload={}, label="📎 Upload a document")


async def process_files(files):
    for file in files:
        await cl.Message(content=f"📄 Processing **{file.name}**...").send()
        chunks = load_and_split_document(file.path)
        vs.add_documents(chunks)
        await cl.Message(
            content=f"✅ **{file.name}** processed — {len(chunks)} chunks added."
        ).send()
    cl.user_session.set("pdf_ready", True)


@cl.on_chat_start
async def start():
    cl.user_session.set("pdf_ready", False)

    files = await cl.AskFileMessage(
        content="Please upload a PDF, DOCX, or TXT file to get started.",
        accept=ACCEPTED_TYPES,
        max_size_mb=20,
        max_files=5,
    ).send()

    if files:
        await process_files(files)

    await cl.Message(
        content="Ask me anything about your document(s). You can upload more anytime.",
        actions=[upload_action()],
    ).send()


@cl.action_callback("upload_more")
async def on_upload_more(action: cl.Action):
    files = await cl.AskFileMessage(
        content="Upload another PDF, DOCX, or TXT file.",
        accept=ACCEPTED_TYPES,
        max_size_mb=20,
        max_files=5,
    ).send()

    if files:
        await process_files(files)

    await cl.Message(content="Document added.", actions=[upload_action()]).send()


@cl.on_message
async def main(message: cl.Message):
    if not cl.user_session.get("pdf_ready"):
        await cl.Message(
            content="Please upload a document first.",
            actions=[upload_action()],
        ).send()
        return

    response = await ask_agent(message.content)
    await cl.Message(content=response, actions=[upload_action()]).send()