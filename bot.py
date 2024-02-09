import asyncio
import os
import re
import twitchio
import openai
from twitchio.ext import commands
from functions import *

bot = commands.Bot(
    token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL'], '#gold_manchannel', '#jastintw', ]
)


async def get_username(user_id, bot):
    try:
        user = await bot.get_user(user_id)
        return user.name
    except twitchio.dataclasses.errors.HTTPError:
        return f"UnknownUser_{user_id}"


user_data = load_user_data()
openai.api_key = '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'


# --------------------------------------------------------------------------------

@bot.event
async def event_ready():
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


@bot.command(name='info')
async def info(ctx):
    await ctx.send(
        f'➺Список глобальных команд: !about - о боте, !лотерея - сыграть в лотерею, !password - угадать пароль как в смертелки[Версия 0.0.1], !pisuninfo - узнать инфу о выращивании писюна, !iqinfo - для саморазвития, !другое - другое(логично)')


@bot.command(name='about')
async def about(ctx):
    await ctx.send(
        f'*̥˚Этот бот создан пользователем ༺@mirka_m_ чисто в развлекательных целях. Не подлежит владению посторонними лицами')


@bot.command(name='pisuninfo')
async def pisuninfo(ctx):
    await ctx.send(f'!pisun - узнать судьбу писюна на сегодня, !mypisun - размер писюна, !top10 - рейтинг писюнов, !top-10 - рейтинг писюнов в жопе')


@bot.command(name='другое')
async def info(ctx):
    await ctx.send(
        f'➺Список команд: !подарок - получите подарок от маленькой девочки, !смэрт - узнайте свою дату смерти, !голос - если не знаете, какую игру выбрать, !askgpt [текст] - пообщайтесь с chatGPT')


@bot.command(name='iqinfo')
async def pisuninfo(ctx):
    await ctx.send(
        f'*̥˚За идею, какой фигней пострадать на стриме, отдаем должное @easygoy. !mpenis - размер писюна, !mmyiq - твой iq, !mboobs - размер бубс, !потвори - повторить текст')


# --------------------------------------------------------------------------------

@bot.command(name='подарок')
async def getgift(ctx):
    await ctx.send(f'{ctx.author.name}, это для тебя 👉👈 🎁 ')


@bot.command(name='смэрт')
async def datesmert(ctx):
    current_year = datetime.now().year
    random_year = random.randint(current_year, current_year + 126)
    random_date = datetime(random_year, random.randint(1, 12), random.randint(1, 28))
    await ctx.send(f'{ctx.author.name}, твоя смерть наступит {random_date.strftime("%d.%m.%Y")}')


# --------------------------------------------------------------------------------

@bot.command(name='askgpt')
async def ask_gpt(ctx, *, user_input):
    chat_history.history.append(f"User: {user_input}")
    chat_history.history = chat_history.history[-3:]
    input_prompt = "\n".join(chat_history.history)

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=input_prompt,
            max_tokens=100
        )

        generated_text = response['choices'][0]['text'].strip()

        if generated_text.startswith("Bot:"):
            generated_text = generated_text[len("Bot:"):].strip()

        if response['usage']['total_tokens'] >= 100:
            match = re.search(r'\.', generated_text)
            if match:
                generated_text = generated_text[:match.end()]

        chat_history.history.append(f"Bot: {generated_text}")
        await ctx.send(generated_text)

    except openai.error.OpenAIError as e:
        await ctx.send(f"Ой бляяяяяяя...: {str(e)}")


# --------------------------------------------------------------------------------

lottery_started = False
correct_numbers = random.sample(range(1, 10), 2)
selected_numbers = []
lottery_starter = None


@bot.command(name='лотерея')
async def start_lottery(ctx):
    global lottery_started, correct_numbers, selected_numbers, lottery_starter

    if not lottery_started:
        lottery_started = True
        lottery_starter = ctx.author.name
        correct_numbers = random.sample(range(1, 10), 2)
        selected_numbers = []
        await ctx.send(
            f'*̥˚Лотерея! Выберите число от 1 до 9 с помощью команды !л [число]. Нужно получить 7 денюжек. Если попадете в хоть один череп, вы лох')

        await asyncio.sleep(120)

        if lottery_started:
            lottery_started = False
            await ctx.send('Ну и идите нахуй! Игра окончена')
            return


@bot.command(name='л')
async def play_lottery(ctx, number: int):
    global lottery_started, correct_numbers, selected_numbers, lottery_starter

    if lottery_started and ctx.author.name == lottery_starter:
        if number in selected_numbers:
            await ctx.send(f'Это число уже было!')
        elif 1 <= number <= 9:
            selected_numbers.append(number)
            if number in correct_numbers:
                await ctx.send(f'Вы лох!')
                lottery_started = False
            elif len(selected_numbers) == 7:
                await ctx.send(f'Вы выиграли эту жизнь. Держите конфетку 🍬')
                lottery_started = False
            else:
                await ctx.send(f'Число {number} $')
        else:
            await ctx.send('Введите число от 1 до 9.')
    elif not lottery_started:
        await ctx.send('Лотерея еще не началась. Введите !лотерея, чтобы начать!')
    else:
        await ctx.send('Вы ху?')


# --------------------------------------------------------------------------------

@bot.command(name='pisun')
async def manipulate_pisun(ctx):
    user_name = ctx.author.name
    user_id = ctx.author.id

    if user_name not in user_data:
        user_data[user_name] = {'rating': 0, 'last_command_time': datetime.now() - timedelta(hours=6),
                                'user_id': user_id}

    remove_inactive_users(user_data)
    current_time = datetime.now()
    last_command_time = user_data[user_name]['last_command_time']
    last_command_username = user_data[user_name].get('last_command_username', user_name)

    if (current_time - last_command_time).total_seconds() >= 6 * 60 * 60:
        change_amount = random.choices(range(-10, 11), weights=[30] * 10 + [70] * 11)[0]
        user_data[user_name]['rating'] += change_amount
        user_data[user_name]['last_command_time'] = current_time
        user_data[user_name]['last_change_amount'] = change_amount
        user_data[user_name]['last_command_username'] = user_name
        user_data[user_name]['user_id'] = user_id

        if change_amount > 0:
            await ctx.send(f'{user_name}, ваш писюн вырос на {change_amount} см! 👀')
        elif change_amount < 0:
            await ctx.send(f'{user_name}, ваш писюн отрезали на {abs(change_amount)} см! ✂')
        else:
            await ctx.send(f'{user_name}, мы потеряли вашу банковскую карту. 0 см')

        if user_data[user_name]['user_id'] == user_id and last_command_username != user_name:
            try:
                await ctx.author.edit(nick=user_name)
            except Exception as e:
                print(f"Брух: {e}")

        save_user_data(user_data)
    else:
        time_remaining = (last_command_time + timedelta(hours=6) - current_time).total_seconds()
        hours, minutes, seconds = format_time(time_remaining)
        await ctx.send(
            f'{last_command_username}, ваша очередь на прием наступит через {hours} часов, {minutes} минут, {seconds} секунд')


@bot.command(name='top10')
async def show_ratings(ctx):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['rating'], reverse=True)[:10]

    ratings_msg = '⇢Рейтинг писюнов⇠ : \n'
    for i, (user_name, data) in enumerate(sorted_users, 1):
        last_command_username = user_data[user_name].get('last_command_username', user_name)
        user_id = user_data[user_name].get('user_id', 'UnknownID')

        ratings_msg += f'{i}. {last_command_username}: {data["rating"]} см \n'

    await ctx.send(ratings_msg)


@bot.command(name='top-10')
async def show_ratings(ctx):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['rating'], reverse=False)[:10]

    ratings_msg = '⇢Рейтинг писюнов⇠ : \n'
    for i, (user_name, data) in enumerate(sorted_users, 1):
        last_command_username = user_data[user_name].get('last_command_username', user_name)
        user_id = user_data[user_name].get('user_id', 'UnknownID')

        ratings_msg += f'{i}. {last_command_username}: {data["rating"]} см \n'

    await ctx.send(ratings_msg)


@bot.command(name='mypisun')
async def show_user_pisun(ctx):
    user_name = ctx.author.name

    if user_name not in user_data:
        user_data[user_name] = {'rating': 0, 'last_command_time': datetime.now() - timedelta(days=1)}

    user_rating = user_data[user_name]['rating']
    last_change_amount = user_data[user_name].get('last_change_amount', 0)

    last_command_username = user_data[user_name].get('last_command_username', user_name)
    await ctx.send(f'{last_command_username}, размер вашего писюна {user_rating} см.')

    user_data[user_name]['last_change_amount'] = last_change_amount
    user_data[user_name]['last_command_username'] = last_command_username
    save_user_data(user_data)


# --------------------------------------------------------------------------------

@bot.command(name='mpenis')
async def mpenis(ctx):
    user_name = ctx.author.name
    penis_size = random.randint(0, 55)
    if 50 <= penis_size <= 55 or penis_size == 0:
        paschal_text = get_paschal_message(penis_paschal, penis_size)
        await ctx.send(f'{user_name}, твой писюн:\n {paschal_text}')
    else:
        paschal_text = get_paschal_message(penis_paschal, penis_size)
        await ctx.send(f'{user_name}, твой писюн: {penis_size} см\n {paschal_text}')


@bot.command(name='mmyiq')
async def mmyiq(ctx):
    user_name = ctx.author.name
    iq = random.randint(-1, 300)
    paschal_text = get_paschal_message(iq_paschal, iq)
    await ctx.send(f'{user_name}, твой IQ {iq}\n {paschal_text}!')


@bot.command(name='mboobs')
async def mboobs(ctx):
    user_name = ctx.author.name
    boobs_size = random.randint(0, 5)

    if boobs_size == 0:
        paschal_text = get_paschal_message(boobs_paschal, boobs_size)
        await ctx.send(f'{user_name}, размер твоих бубс: {paschal_text}')
    else:
        paschal_text = get_paschal_message(boobs_paschal, boobs_size)
        await ctx.send(f'{user_name}, размер твоих бубс: {boobs_size}\n {paschal_text}')


# --------------------------------------------------------------------------------

@bot.command(name='повтори')
async def repeat_message(ctx, *, message):
    if message.lower() in voices:
        await ctx.send("🖕")
    else:
        await ctx.send(message)


@bot.command(name='голос')
async def voice_command(ctx):
    selected_voice = random.choice(voices)
    await ctx.send(f'Выбор: {selected_voice}')


# --------------------------------------------------------------------------------

password_game = PasswordGame()
game_in_progress = False


@bot.command(name='password')
async def start_game(ctx):
    global game_in_progress

    if not game_in_progress:
        password_game.__init__()
        game_in_progress = True
        await ctx.send('?Вы из этих задротов в смертелку? !п [Слово из 4 букв]')
    else:
        await ctx.send('Игра уже начата. Введите !ответ, чтобы завершить текущую игру.')


@bot.command(name='п')
async def make_guess(ctx, *, guess: str):
    global game_in_progress

    if game_in_progress:
        if len(guess) == 4 and guess.isalpha():
            guess = guess.lower()

            for i in range(4):
                if i < len(password_game.password) and guess[i] == password_game.password[i]:
                    password_game.correct_guesses.add(i)

            if len(password_game.correct_guesses) == 4:
                await ctx.send(f'{ctx.author.name}, ты умный. Игра окончена')
                password_game.__init__()
                game_in_progress = False
        else:
            await ctx.send('Ноуп')

        partial_password_message = password_game.display_partial_password()
        await ctx.send(partial_password_message)
    else:
        await ctx.send('Игра еще не начата. Введите !password, чтобы начать новую игру.')


@bot.command(name='ответ')
async def end_game(ctx):
    global game_in_progress

    if game_in_progress:
        await ctx.send(f'Игра закончена. Правильный пароль: {password_game.password}')
        password_game.__init__()
        game_in_progress = False
    else:
        await ctx.send('Игра еще не началась. Введите !password, чтобы начать новую игру.')


if __name__ == "__main__":
    bot.run()
