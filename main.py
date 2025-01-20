import asyncio
from My_Models import Use_model



async def worker(my_model):
    """Worker loop that continuously processes the queue."""
    while True:
        if not my_model.queue.empty():
            await my_model.update()  # Process one item
        await asyncio.sleep(0.1)  # Avoid busy-waiting



async def main():
    # Initialize the model
    my_model = Use_model(ver="V1")

    # Start the worker loop
    worker_task = asyncio.create_task(worker(my_model))

    # Store unique IDs for reference
    unique_ids = {}

    print("Ready for input commands.")
    print('Commands:',
          '\n - "R" to read a text and add to the queue.',
          '\n - "W" to write summary by unique ID.',
          '\n - Press Enter to continue processing.')

    while True:
        # Wait for user input
        user_input = input("Enter command: ").strip()

        if user_input.upper() == "R":
            # Add text to the queue
            text = input("Enter text to add to queue: ").strip()
            if text:
                unique_id = await my_model.add_to_queue(text)
                print(f"Added to queue with unique ID: {unique_id}")
                unique_ids[text] = unique_id
            else:
                print("No text provided. Skipping.")


        elif user_input.upper() == "W":
            # Write the summary for a given unique ID
            unique_id = input("Enter unique ID to retrieve summary: ").strip()
            found_status, found_summary = await my_model.find_summary_by_id(unique_id)
            if found_status:
                print(f"Summary for ID {unique_id}:\n\n{found_summary}\n")
            else:
                print(f"No summary found for ID {unique_id}")


        elif user_input == "":
            # Continue processing the queue
            print("Processing queue... Press Ctrl+C to stop.")
            await asyncio.sleep(0.1)  # Allow the worker to process items

        elif user_input.upper() == "EXIT":
            print("Exiting program")
            await worker_task
            break


        else:
            print("Invalid command. Try again.")

    # Cancel the worker when exiting
    worker_task.cancel()


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
