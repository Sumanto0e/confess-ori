import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import re
import config
from menfess.dk import Dk
from menfess.helpers import Database, Helper
from menfess.helpers import Database



@Dk.on_callback_query(filters.regex('^help$'))
async def help_inline(client: Client, query: CallbackQuery):
    msg = query.message
    pesan = "Supported commands\n"
    pesan += '/status — melihat status\n'
    pesan += '/topup — top up coin\n'
    pesan += '/tf_coin — transfer coin\n'
    pesan += '/rubahstatus — merubah status\n'
    pesan += '/daget — untuk memberikan koin masal penghuni ons\n'

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='https://t.me/menfesonsbase/111'), InlineKeyboardButton('status', callback_data='status'), InlineKeyboardButton('top up', callback_data='topup')]
    ])
    await msg.edit(pesan, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^status$'))
async def status_inline(client: Client, query: CallbackQuery):
    msg = query.message
    helper = Helper(client, msg)
    db = Database(query.from_user.id, client.me.id).get_data_pelanggan()
    pesan ='<b>ID CARD ONS</b>\n\n'
    pesan += f'🆔 <b>ID</b>                  : <code>{db.id}</code>\n\n'
    pesan += f'👮 <b>User</b>              : {db.mention}\n\n'
    pesan += f'👑 <b>Status</b>          : {db.status}\n\n'
    pesan += f'💸 <b>Coin</b>              : {helper.formatrupiah(db.coin)} ONS\n\n'
    pesan += f'📆 <b>Daily Send</b>  : {db.menfess}/{config.batas_kirim}\n\n'

    poson = 'ID CARD ONS\n\n'
    poson += f'🆔 ID                  : {db.id}\n\n'
    poson += f'👮 User              : {db.mention}\n\n'
    poson += f'👑 Status          : {db.status}\n\n'
    poson += f'💸 Coin              : {helper.formatrupiah(db.coin)} ONS\n\n'
    poson += f'📆 Daily Send  : {db.menfess}/{config.batas_kirim}\n\n'


    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Rules', url='https://t.me/menfesonsbase/111'), InlineKeyboardButton('help', callback_data='help'), InlineKeyboardButton('top up', callback_data='topup')]
    ])
    if db.status == 'talent' or db.status == 'member' or db.status == 'girlfriend rent' or db.status == 'proplayer' or db.status == 'teman curhat' or db.status == 'daddy sugar' or db.status == 'boyfriend rent' or db.status == 'sad girl' or db.status == 'melayu' or db.status == 'balinese' or db.status == 'jakartans' or db.status == 'pick me' or db.status == 'borneoensis' or db.status == 'body goals' or db.status == 'abg' or db.status == 'baby girl' or db.status == 'wong jowo' or db.status == 'admin' or db.status == 'owner':
        await msg.edit(poson, reply_markup=markup)

    if db.status == 'non member':
        await msg.edit(pesan, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^photo$'))
async def photo_handler_inline(client: Client, query: CallbackQuery):
    msg = query.message
    inline_keyboard = msg.reply_markup.inline_keyboard[0][1].text
    my_db = Database(msg.from_user.id, client.me.id)
    if inline_keyboard in ['✅', '❌']:
        pesan = "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        pesan += "______________________________\n\n"
        if inline_keyboard == '✅':
            await my_db.photo_handler('✅', client.me.id)
        else:
            await my_db.photo_handler('❌', client.me.id)

        db = my_db.get_data_bot(client.me.id)
        photo = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.photo else ["AKTIF", "✅"]
        video = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.video else ["AKTIF", "✅"]
        voice = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.voice else ["AKTIF", "✅"]
        status_bot = "TIDAK AKTIF" if not db.bot_status else "AKTIF"
        pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
        pesan += f"🎥 Video = <b>{video[0]}</b>\n"
        pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
        pesan += f"🔰Status bot: <b>{status_bot}</b>"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('📸', callback_data='no'), InlineKeyboardButton(photo[1], callback_data='photo')],
            [InlineKeyboardButton('🎥', callback_data='no'), InlineKeyboardButton(video[1], callback_data='video')],
            [InlineKeyboardButton('🎤', callback_data='no'), InlineKeyboardButton(voice[1], callback_data='voice')],
            [InlineKeyboardButton(status_bot, callback_data='status_bot')]
        ])
        await msg.edit(pesan, parse_mode=enums.ParseMode.HTML, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^video$'))
async def video_handler_inline(client: Client, query: CallbackQuery):
    msg = query.message
    inline_keyboard = msg.reply_markup.inline_keyboard[1][1].text
    my_db = Database(msg.from_user.id, client.me.id)
    if inline_keyboard in ['✅', '❌']:
        pesan = "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        pesan += "______________________________\n\n"
        if inline_keyboard == '✅':
            await my_db.video_handler('✅', client.me.id)
        else:
            await my_db.video_handler('❌', client.me.id)

        db = my_db.get_data_bot(client.me.id)
        photo = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.photo else ["AKTIF", "✅"]
        video = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.video else ["AKTIF", "✅"]
        voice = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.voice else ["AKTIF", "✅"]
        status_bot = "TIDAK AKTIF" if not db.bot_status else "AKTIF"
        pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
        pesan += f"🎥 Video = <b>{video[0]}</b>\n"
        pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
        pesan += f'🔰Status bot: <b>{status_bot}</b>'
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('📸', callback_data='no'), InlineKeyboardButton(photo[1], callback_data='photo')],
            [InlineKeyboardButton('🎥', callback_data='no'), InlineKeyboardButton(video[1], callback_data='video')],
            [InlineKeyboardButton('🎤', callback_data='no'), InlineKeyboardButton(voice[1], callback_data='voice')],
            [InlineKeyboardButton(status_bot, callback_data='status_bot')]
        ])
        await msg.edit(pesan, parse_mode=enums.ParseMode.HTML, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^voice$'))
async def voice_handler_inline(client: Client, query: CallbackQuery):
    msg = query.message
    inline_keyboard = msg.reply_markup.inline_keyboard[2][1].text
    my_db = Database(msg.from_user.id, client.me.id)
    if inline_keyboard in ['✅', '❌']:
        pesan = "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        pesan += "______________________________\n\n"
        if inline_keyboard == '✅':
            await my_db.voice_handler('✅', client.me.id)
        else:
            await my_db.voice_handler('❌', client.me.id)

        db = my_db.get_data_bot(client.me.id)
        photo = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.photo else ["AKTIF", "✅"]
        video = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.video else ["AKTIF", "✅"]
        voice = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.voice else ["AKTIF", "✅"]
        status_bot = "TIDAK AKTIF" if not db.bot_status else "AKTIF"
        pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
        pesan += f"🎥 Video = <b>{video[0]}</b>\n"
        pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
        pesan += f'🔰Status bot: <b>{status_bot}</b>'
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('📸', callback_data='no'), InlineKeyboardButton(photo[1], callback_data='photo')],
            [InlineKeyboardButton('🎥', callback_data='no'), InlineKeyboardButton(video[1], callback_data='video')],
            [InlineKeyboardButton('🎤', callback_data='no'), InlineKeyboardButton(voice[1], callback_data='voice')],
            [InlineKeyboardButton(status_bot, callback_data='status_bot')]
        ])
        await msg.edit(pesan, parse_mode=enums.ParseMode.HTML, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^status_bot$'))
async def status_handler_inline(client: Client, query: CallbackQuery):
    if query.from_user.id != config.id_admin:
        return await query.answer('Ditolak, kamu tidak ada akses', True)
    msg = query.message
    inline_keyboard = msg.reply_markup.inline_keyboard[3][0].text
    my_db = Database(msg.from_user.id, client.me.id)
    if inline_keyboard in ['AKTIF', 'TIDAK AKTIF']:
        pesan = "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        pesan += "______________________________\n\n"
        if inline_keyboard == 'AKTIF':
            await my_db.bot_handler('off')
        else:
            await my_db.bot_handler('on')

        db = my_db.get_data_bot(client.me.id)
        photo = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.photo else ["AKTIF", "✅"]
        video = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.video else ["AKTIF", "✅"]
        voice = ["TIDAK AKTIF", "❌"] if not db.kirimchannel.voice else ["AKTIF", "✅"]
        status_bot = "TIDAK AKTIF" if not db.bot_status else "AKTIF"
        pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
        pesan += f"🎥 Video = <b>{video[0]}</b>\n"
        pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
        pesan += f'🔰Status bot: <b>{status_bot}</b>'
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('📸', callback_data='no'), InlineKeyboardButton(photo[1], callback_data='photo')],
            [InlineKeyboardButton('🎥', callback_data='no'), InlineKeyboardButton(video[1], callback_data='video')],
            [InlineKeyboardButton('🎤', callback_data='no'), InlineKeyboardButton(voice[1], callback_data='voice')],
            [InlineKeyboardButton(status_bot, callback_data='status_bot')]
        ])
        await msg.edit(pesan, parse_mode=enums.ParseMode.HTML, reply_markup=markup)


@Dk.on_callback_query(filters.regex('^hapus-'))
async def hapus_inline(client: Dk, query: CallbackQuery):
    uid = query.from_user.id
    if uid == 0:
        return await query.answer("Invalid user id")
    if len(query.data) < 2:
        return await query.answer("Invalid message id")
    db = Database(uid, client.me.id)
    msg_id = query.data.split("-")[1]
    user = db.get_data_pelanggan()
    current_coin = user.coin
    harga = config.biaya_delete
    if current_coin < harga:
        return await query.answer("Koin anda tidak mencukupi untuk menghapus anda dikenakan biaya 25coin", show_alert=True)
    new_coin = user.coin - harga
    await db.update_coin(new_coin)
    deleted = await client.delete_messages(client.channel_1, int(msg_id))
    if deleted:
        await query.message.edit_text("✅ Pesan Telah Dihapus", reply_markup=None)
        return await query.answer(f"Postingan berhasil dihapus, koin kamu berkurang {harga}", show_alert=True)