from core import types, InlineKeyboardBuilder, quiz_data, aiosqlite, DB_NAME


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]["correct_option"]
    opts = quiz_data[current_question_index]["options"]
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(
        f"{quiz_data[current_question_index]['question']}", reply_markup=kb
    )


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(
            types.InlineKeyboardButton(
                text=option,
                callback_data=(
                    f"right_answer{option}"
                    if option == right_answer
                    else f"wrong_answer{option}"
                ),
            )
        )

    builder.adjust(1)
    return builder.as_markup()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT question_index FROM quiz_state WHERE user_id = (?)", (user_id,)
        ) as cursor:

            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
