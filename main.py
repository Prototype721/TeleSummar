import asyncio
from My_Models import Use_model



async def worker(my_model):
    """Цикл для обработки значений моделью в свободное время"""
    while True:
        if not my_model.queue.empty():
            await my_model.update()  # Обработка одного значения в очереди
        await asyncio.sleep(0.1)  # Выход из очереди (?) | TODO 1



async def main():
    # Выбор модели для работы
    my_model = Use_model(ver="V1")

    # Запуск worker для подсчёта моделью текстов в очереди
    worker_task = asyncio.create_task(worker(my_model))

    # Хранение всех уникальных ID
    unique_ids = {}

    print("Ready for input commands.")
    print('Commands:',
          '\n - "R" to read a text and add to the queue.',
          '\n - "W" to write summary by unique ID.',
          '\n - Press Enter to continue processing.',
          '\n - "EXIT" for exit the program')

    while True:

        # Выбор режима работы
        user_input = input("Enter command: ").strip()

        if user_input.upper() == "R":
            # Добавление текста для обработки в очередь (связный список)

            text = input("Enter text to add to queue: ").strip()
            if text:
                unique_id = await my_model.add_to_queue(text)
                print(f"Added to queue with unique ID: {unique_id}")
                unique_ids[text] = unique_id
            else:
                print("No text provided. Skipping.")


        elif user_input.upper() == "W":
            # Вывод результата сокращения с ID через хэш-таблицу (словарь)

            unique_id = input("Enter unique ID to retrieve summary: ").strip()
            found_status, found_summary = await my_model.find_summary_by_id(unique_id)
            if found_status:
                print(f"Summary for ID {unique_id}:\n\n{found_summary}\n")
            else:
                print(f"No summary found for ID {unique_id}")


        elif user_input == "":
            # Подсчёт моделью текстов в очереди

            print("Processing queue... Press Ctrl+C to stop.")
            await asyncio.sleep(0.1)  # Позволяет worker обработать один запрос                                         # TODO: 1) Добавить прерывание процесса не через Ctrl+C

        elif user_input.upper() == "EXIT":                                                                              # TODO: 3) Настроить выход
            # Выход из цикла с очисткой памяти

            print("Exiting program")
            await worker_task
            break


        else:
            print("Invalid command. Try again.")

    # Закончить работу worker_task
    worker_task.cancel()



if __name__ == "__main__":
    asyncio.run(main())
