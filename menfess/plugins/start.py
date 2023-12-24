import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import re
import config
from menfess.dk import Dk
from menfess.helpers import Database, Helper
from menfess.helpers.decorators import Bot
from menfess.helpers.referral import ReferralDB, add_by_referral, new_referral, invite_handler
from menfess.helpers import Database


@Bot("start")
async def on_start_handler(client: Client, msg: Message, db: Database = None):
    is_new = False
    helper = Helper(client, msg)
    if db and not await db.cek_user_didatabase():  # cek apakah user sudah ditambahkan didatabase
        is_new = True
        await helper.daftar_pelanggan()  # jika belum akan ditambahkan data user ke database
        await helper.send_to_channel_log(type="log_daftar")
    command = msg.text or msg.caption
    _cmd = command.split()
    if is_new and len(_cmd) > 1:
        invite_code = _cmd[1]
        await add_by_referral(client, msg, invite_code)
    await new_referral(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = first if not last else first + ' ' + last
    username = '@nazhak' if not msg.from_user.username else '@' + msg.from_user.username
    mention = msg.from_user.mention
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='https://t.me/menfesonsbase/111')]
    ])
    await msg.reply_text(
        text=config.start_msg.format(
            id=msg.from_user.id,
            mention=mention,
            username=username,
            first_name=await helper.escapeHTML(first),
            last_name=await helper.escapeHTML(last),
            fullname=await helper.escapeHTML(fullname),
        ),
        reply_markup=markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot("status")
async def status_handler(client: Client, msg: Message, db: Database = None):
    helper = Helper(client, msg)
    db = db.get_data_pelanggan()
    ref_db = ReferralDB(msg.from_user.id)
    ref_code = await ref_db.referral()
    link_reff = f"`https://t.me/{client.me.username}?start={ref_code}`"
    pesan = '<b>ID CARD ONS</b>\n\n'
    pesan += f'🆔 <b>ID</b>                  : <code>{db.id}</code>\n\n'
    pesan += f'👮 <b>User</b>              : {db.mention}\n\n'
    pesan += f'👑 <b>Status</b>          : {db.status}\n\n'
    pesan += f'🕵️ Referral Link        : {link_reff}\n\n'
    pesan += f'💸 <b>Coin</b>              : {helper.formatrupiah(db.coin)} ONS\n\n'
    pesan += f'📆 <b>Daily Send</b>  : {db.menfess}/{config.batas_kirim}\n\n'

    poson = 'ID CARD ONS\n\n'
    poson += f'🆔 ID                  : {db.id}\n\n'
    poson += f'👮 User              : {db.mention}\n\n'
    poson += f'👑 Status          : {db.status}\n\n'
    poson += f'🕵️ Referral Link        : {link_reff}\n\n'
    poson += f'💸 Coin              : {helper.formatrupiah(db.coin)} ONS\n\n'
    poson += f'📆 Daily Send  : {db.menfess}/{config.batas_kirim}\n\n'

    caption = msg.text or msg.caption
    entities = msg.entities or msg.caption_entities

    if db.status == 'talent':
        picture = config.pic_talent
    if db.status == 'gf rent':
        picture = config.pic_gfrent
    if db.status == 'proplayer':
        picture = config.pic_proplayer

    if db.status == 'teman curhat':
        picture = config.pic_temancurhat
    if db.status == 'jakartans':
        picture = config.pic_jakartans
    if db.status == 'balinese':
        picture = config.pic_balinese
    if db.status == 'borneoensis':
        picture = config.pic_borneo
    if db.status == 'melayu':
        picture = config.pic_melayu
    if db.status == 'sad girl':
        picture = config.pic_sadgirl
    if db.status == 'body goals':
        picture = config.pic_bodygoals
    if db.status == 'wong jowo':
        picture = config.pic_wongjowo
    if db.status == 'abg':
        picture = config.pic_abg
    if db.status == 'baby girl':
        picture = config.pic_babygirl
    if db.status == 'pick me':
        picture = config.pic_pickme
    if db.status == 'bf rent':
        picture = config.pic_bfrent
    if db.status == 'daddy sugar':
        picture = config.pic_daddysugar

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='https://t.me/menfesonsbase/111'), InlineKeyboardButton('help', callback_data='help'), InlineKeyboardButton('top up', callback_data='topup')]
    ])
    if db.status == 'talent' or db.status == 'girlfriend rent' or db.status == 'proplayer' or db.status == 'teman curhat' or db.status == 'daddy sugar' or db.status == 'boyfriend rent' or db.status == 'sad girl' or db.status == 'melayu' or db.status == 'balinese' or db.status == 'jakartans' or db.status == 'pick me' or db.status == 'borneoensis' or db.status == 'body goals' or db.status == 'abg' or db.status == 'baby girl' or db.status == 'wong jowo':
        await client.send_photo(db.id, picture, poson, caption_entities=entities, reply_markup=markup)

    if db.status == 'member' or db.status == 'admin' or db.status == 'owner':
        await client.send_message(db.id, poson, reply_markup=markup)

    if db.status == 'non member':
        await client.send_message(db.id, pesan, reply_markup=markup)


@Bot("rubahstatus")
async def rubahstatus_handler(client: Client, msg: Message, db: Database = None):
    pesan = 'Chat @leoopttt jika anda ingin merubah status anda. Check status yang tersedia di @statusonsbase'
    await msg.reply(pesan, True, enums.ParseMode.HTML)

@Bot("stats", is_admin=True)
async def statistik_handler(client: Client, msg: Message, db: Database = None):
    bot = db.get_data_bot(client.me.id)
    db_user = db.get_data_pelanggan()
    pesan = "<b>📊 STATISTIK BOT\n\n"
    pesan += f"▪️Pelanggan: {db.get_pelanggan().total_pelanggan}\n"
    pesan += f"▪️Admin: {len(bot.admin)}\n"
    pesan += f"▪️Talent: {len(bot.talent)}\n"
    pesan += f"▪️Daddy sugar: {len(bot.daddy_sugar)}\n"
    pesan += f"▪️Proplayer: {len(bot.proplayer)}\n"
    pesan += f"▪️Teman Curhat: {len(bot.temancurhat)}\n"
    pesan += f"▪️Girlfriend rent: {len(bot.gfrent)}\n"
    pesan += f"▪️Boyfriend rent: {len(bot.bfrent)}\n"
    pesan += f"▪️Banned: {len(bot.ban)}\n\n"
    pesan += f"🔰Status bot: {'AKTIF' if bot.bot_status else 'TIDAK AKTIF'}</b>"
    await msg.reply_text(pesan, True, enums.ParseMode.HTML)


@Bot("/reff")
async def on_reff_handler(client: Client, msg: Message, database: Database = None):
    return await invite_handler(client, msg)