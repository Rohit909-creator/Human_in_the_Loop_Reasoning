import ollama

def interactive_chat():
    messages = [
        {"role": "user", "content": "Who is the king of the jungle?"}
    ]

    while True:
        response = ollama.chat(
            model="deepseek_finetuned_model",
            messages=messages,
            stream=True
        )

        buffer = ""
        assistant_response = ""  # capture assistant output this round

        for chunk in response:
            token = chunk["message"]["content"]
            buffer += token

            # Check tags
            for tag in ["</ask>", "</question>", "</doubt>"]:
                if tag in buffer:
                    before, _, after = buffer.partition(tag)

                    # Save assistant’s response up to this tag
                    if before.strip():
                        print(before.strip(), end="", flush=True)
                        assistant_response += before.strip()

                    # Add assistant response so far to messages
                    messages.append({"role": "assistant", "content": assistant_response})

                    # Get user input
                    user_input = input("\n👉 Model is asking you something: ")

                    # Add user reply
                    messages.append({"role": "user", "content": user_input})

                    # Reset buffer and restart chat loop
                    buffer = after
                    break
            else:
                # If no tag found in this token, keep streaming
                print(token, end="", flush=True)
                assistant_response += token
                continue

            # If a tag was found, stop current response loop and restart
            break

        else:
            # End of stream, push remaining assistant response to history
            if buffer.strip():
                print(buffer, end="", flush=True)
                assistant_response += buffer.strip()

            if assistant_response.strip():
                messages.append({"role": "assistant", "content": assistant_response})

            break  # fully done, no <ask>/<question>/<doubt> left


if __name__ == "__main__":
    interactive_chat()