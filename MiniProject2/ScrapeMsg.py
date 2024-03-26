import asyncio
import configparser
import pandas as pd
from datetime import datetime, timedelta

from telethon import TelegramClient, errors

async def extract_messages(client, channel, start_date, end_date):
    messages = await client.get_messages(channel, limit=None)
    filtered_messages = [msg for msg in messages if start_date <= msg.date.date() <= end_date]
    return filtered_messages

async def main():
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    async with TelegramClient(username, api_id, api_hash) as client:
        await client.start()
        print("Client Created")

        # Ensure you're authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except errors.SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        channel_name = 'Merademy'
        end_date = datetime.now().date()  # Current date
        start_date = end_date - timedelta(days=7)  # One week before current date

        channel = await client.get_entity(channel_name)
        messages = await extract_messages(client, channel, start_date, end_date)

        if messages:
            # Create DataFrame with necessary attributes
            data = [{'date': msg.date, 'message': msg.message} for msg in messages]
            df = pd.DataFrame(data)

            # Ensure 'date' column is of datetime type
            df['date'] = pd.to_datetime(df['date'])

            # Remove timezone information
            df['date'] = df['date'].dt.tz_localize(None)

            file_name = f'data_{channel_name}_{start_date.strftime("%Y-%m-%d")}_to_{end_date.strftime("%Y-%m-%d")}.csv'
            df.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")
        else:
            print(f"No messages found in {channel_name} from {start_date} to {end_date}")

asyncio.run(main())
