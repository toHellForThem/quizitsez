from core import types, Command, F, ReplyKeyboardBuilder, quiz_data
from reload import get_question, get_quiz_index
from connect import (
    update_quiz_index,
    new_quiz,
    get_user_score,
    update_user_score,
    get_statistics,
)


def setListeners(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        await message.answer(
            "Добро пожаловать в квиз!",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )

    @dp.callback_query(F.data.contains("right_answer"))
    async def right_answer(callback: types.CallbackQuery):
        await callback.message.answer(callback.data.replace("right_answer", ""))
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None,
        )
        await callback.message.answer("Верно!")

        current_question_index = await get_quiz_index(callback.from_user.id)
        current_question_index += 1

        user_score = await get_user_score(callback.from_user.id)
        user_score += 1

        await update_quiz_index(
            callback.from_user.id, callback.from_user.username, current_question_index
        )
        await update_user_score(callback.from_user.id, user_score)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, callback.from_user.id)
        else:
            await callback.message.answer(
                f"Это был последний вопрос. Квиз завершен! Ваш результат: {user_score}! Для вывода статистики всех игроков используйте /state"
            )

    @dp.callback_query(F.data.contains("wrong_answer"))
    async def wrong_answer(callback: types.CallbackQuery):
        await callback.message.answer(callback.data.replace("wrong_answer", ""))
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None,
        )

        current_question_index = await get_quiz_index(callback.from_user.id)
        correct_option = quiz_data[current_question_index]["correct_option"]

        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
        )

        current_question_index += 1

        user_score = await get_user_score(callback.from_user.id)
        await update_quiz_index(
            callback.from_user.id, callback.from_user.username, current_question_index
        )
        await update_user_score(callback.from_user.id, user_score)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, callback.from_user.id)
        else:
            await callback.message.answer(
                f"Это был последний вопрос. Квиз завершен! Ваш результат: {user_score}! Для вывода статистики всех игроков используйте /state"
            )

    @dp.message(F.text == "Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer(f"Давайте начнем квиз!")
        await new_quiz(message)

    @dp.message(Command("state"))
    async def cmd_state(message: types.Message):
        message_str = "Статистика игроков\n ----------------------------------------\n"
        results = await get_statistics()

        for s in results:
            message_str += s[0] + " - " + str(s[1]) + "\n"

        await message.answer(message_str)
