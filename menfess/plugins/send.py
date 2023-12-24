import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, Chat
import re
import config
from menfess import is_bad
from menfess.dk import Dk
from menfess.helpers import Database, Helper
from menfess.helpers.decorators import Bot
from menfess.helpers.referral import ReferralDB
from menfess.helpers import Database


async def send_menfess_handler(client: Dk, msg: Message):
    helper = Helper(client, msg)
    db = Database(msg.from_user.id, client.me.id)
    db_user = db.get_data_pelanggan()
    db_bot = db.get_data_bot(client.me.id).kirimchannel
    if msg.text or msg.photo or msg.video or msg.voice:
        if msg.photo and not db_bot.photo:
            if db_user.status == 'member' or db_user.status == 'talent' or db_user.status == 'non member' or db_user.status == 'daddy sugar':
                return await msg.reply('Tidak bisa mengirim photo, karena sedang dinonaktifkan oleh admin', True)
        elif msg.video and not db_bot.video:
            if db_user.status == 'member' or db_user.status == 'talent' or db_user.status == 'non member' or db_user.status == 'daddy sugar':
                return await msg.reply('Tidak bisa mengirim video, karena sedang dinonaktifkan oleh admin', True)
        elif msg.voice and not db_bot.voice:
            if db_user.status == 'member' or db_user.status == 'talent' or db_user.status == 'non member' or db_user.status == 'daddy sugar':
                return await msg.reply('Tidak bisa mengirim voice, karena sedang dinonaktifkan oleh admin', True)

        menfess = db_user.menfess
        all_menfess = db_user.all_menfess
        coin = db_user.coin
        if menfess >= config.batas_kirim:
            if db_user.status == 'member' or db_user.status == 'talent' or db_user.status == 'non member' or db_user.status == 'girlfriend rent' or db_user.status == 'proplayer' or db_user.status == 'teman curhat' or db_user.status == 'daddy sugar' or db_user.status == 'boyfriend rent' or db_user.status == 'sad girl' or db_user.status == 'melayu' or db_user.status == 'balinese' or db_user.status == 'jakartans' or db_user.status == 'pick me' or db_user.status == 'borneoensis' or db_user.status == 'body goals' or db_user.status == 'abg' or db_user.status == 'baby girl' or db_user.status == 'wong jowo':
                if coin >= config.biaya_kirim:
                    coin = db_user.coin - config.biaya_kirim
                else:
                    return await msg.reply(
                        f'🙅🏻‍♀️ <b>Pesan Gagal Terkirim</b> karena <b>Daily send</b> kamu telah habis serta <b>coin</b> mu kurang dari <b>100 ONS</b> untuk mengirim menfess, segera cek /status kamu.\n\n<b>Daily send</b> direset setiap jam 1 pagi\n\n<b>Menjadi member mendapatkan 5 daily send</b>\n\Dapatkan dailysend dan coin gratis dengan link anda:\n\n https://t.me/CONFESONSBOT?start=INV{db_user.id}\n\nBaca ketentuannya di @CONFESONSBOT lalu ketik /reff',
                        quote=True)
        if db_user.status == 'talent':
            picture = config.pic_talent
        if db_user.status == 'gf rent':
            picture = config.pic_gfrent
        if db_user.status == 'proplayer':
            picture = config.pic_proplayer
        if db_user.status == 'teman curhat':
            picture = config.pic_temancurhat
        if db_user.status == 'jakartans':
            picture = config.pic_jakartans
        if db_user.status == 'balinese':
            picture = config.pic_balinese
        if db_user.status == 'borneoensis':
            picture = config.pic_borneo
        if db_user.status == 'melayu':
            picture = config.pic_melayu
        if db_user.status == 'sad girl':
            picture = config.pic_sadgirl
        if db_user.status == 'body goals':
            picture = config.pic_bodygoals
        if db_user.status == 'wong jowo':
            picture = config.pic_wongjowo
        if db_user.status == 'abg':
            picture = config.pic_abg
        if db_user.status == 'baby girl':
            picture = config.pic_babygirl
        if db_user.status == 'pick me':
            picture = config.pic_pickme
        if db_user.status == 'bf rent':
            picture = config.pic_bfrent
        if db_user.status == 'daddy sugar':
            picture = config.pic_daddysugar
        chat = await client.get_chat(client.channel_1)
        link = await get_link(chat)
        kirim = await client.copy_message(client.channel_1, msg.from_user.id, msg.id)
        linkk = link + str(kirim.id)
        linkkk = linkk + "?comment=" + str(kirim.id)
        await helper.send_to_channel_log(type="log_channel", link=link + str(kirim.id))
        await db.update_menfess(coin, menfess, all_menfess)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Check postingan', url=linkk), InlineKeyboardButton('Check comment', url=linkkk)],
            [InlineKeyboardButton('Hapus Postingan', callback_data=f"hapus-{kirim.id}")]
        ])
        await client.send_message(msg.from_user.id,
                                  f"✅ Pesan Telah Berhasil Terkirim\n\n<b>Beli merchandise kami <a href='shopee.co.id/umbrellaspesies'>disini</a>\n\n<a href='https://www.instagram.com/abdimas_hermawan/'>Instagram</a> | <a href='https://www.tiktok.com/@user029284859'>TikTok</a> | <a href='https://www.youtube.com/@nazhaktv6823/featured'>Youtube</a>",
                                  reply_markup=markup, disable_web_page_preview=True)
        await client.send_message(msg.from_user.id,
                                  f"{msg.from_user.first_name} ingin mendapatkan lebih banyak comment?\n#onsbase\n📷❤️😍 tiktok.com/tag/onsbase\n\nDonasi video anda ke @tiktokonsbot untuk di post <a href='https://www.tiktok.com/@onsbase'>disini</a>",
                                  disable_web_page_preview=True)
    else:
        await msg.reply('media yang didukung photo, video dan voice')


async def get_link(chat: Chat) -> str:
    link = f"https://t.me/{chat.username}/" if chat.username else f"https://t.me/c/{chat.id}/"
    return link


@Bot(r"^[\/]tf_coin", regex=True, flt=(filters.group | filters.private))
async def on_transfer_coin_handler(client: Dk, msg: Message, db: Database = None):
    uid = msg.from_user.id
    helper = Helper(client, msg)
    if msg.chat.type == enums.ChatType.GROUP or msg.chat.type == enums.ChatType.SUPERGROUP:
        if not await helper.cek_join_channel(uid):
            try:
                get_chat = await client.get_chat(client.channel_1)
                link = await get_link(get_chat)
                await client.delete_messages(msg.chat.id, msg.id)
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton('Channel base', url=link)]
                ])
                sumonta = await client.send_message(client.channel_log, f"@{msg.from_user.username}\n\n<b>Tidak dapat mengirim pesan, harap join {get_chat.username} terlebih dahulu</b>", reply_markup=markup)
                await asyncio.sleep(60)
                return await sumonta.delete(revoke=True)
            except:
                pass
    if re.search(r"^[\/]tf_coin(\s|\n)*$", msg.text or msg.caption):
        err = "<i>perintah salah /tf_coin [jmlh_coin]</i>" if msg.reply_to_message else "<i>perintah salah /tf_coin [id_user] [jmlh_coin]</i>"
        return await msg.reply(err, True)
    coin = 0
    target = 0
    if re.search(r"^[\/]tf_coin\s(\d+)(\s(\d+))?", msg.text or msg.caption):
        x = re.search(r"^[\/]tf_coin\s(\d+)(\s(\d+))$", msg.text or msg.caption)
        if x:
            target = x.group(1)
            coin = x.group(3)
        y = re.search(r"^[\/]tf_coin\s(\d+)$", msg.text or msg.caption)
        if y:
            if msg.reply_to_message:
                if msg.reply_to_message.from_user.is_bot == True:
                    return await msg.reply('🤖Bot tidak dapat ditranfer coin', True)
                elif msg.reply_to_message.sender_chat:
                    return await msg.reply('channel tidak dapat ditranfer coin', True)
                else:
                    target = msg.reply_to_message.from_user.id
                    coin = y.group(1)
            else:
                return await msg.reply('sambil mereply sebuah pesan', True)

        if msg.from_user.id == int(target):
            return await msg.reply('<i>Tidak dapat transfer coin untuk diri sendiri</i>', True)

        user_db = db
        anu = user_db.get_data_pelanggan()
        my_coin = anu.coin
        if my_coin >= int(coin):
            db_target = Database(int(target), client.me.id)
            if await db_target.cek_user_didatabase():
                target_db = db_target.get_data_pelanggan()
                ditransfer = my_coin - int(coin)
                diterima = target_db.coin + int(coin)
                nama = "Admin" if anu.status == 'owner' or anu.status == 'admin' else msg.from_user.first_name
                nama = await helper.escapeHTML(nama)
                nami = target
                nanti = await helper.escapeHTML(nami)
                try:
                    await client.send_message(target,
                                              f"Coin berhasil ditambahkan senilai {coin} coin, cek /status\n└Oleh <a href='tg://user?id={msg.from_user.id}'>{nama}</a>")
                    await user_db.transfer_coin(ditransfer, diterima, target_db.coin_full, int(target))
                    await msg.reply(f'<i>berhasil transfer coin sebesar {coin} coin💰</i>', True)
                    await client.send_message(client.channel_tf,
                                              f"Coin berhasil ditambahkan senilai {coin} coin) dari <a href='tg://user?id={msg.from_user.id}'>{nama}</a> ke <a href='tg://user?id={target}'>{nanti}</a>")
                except Exception as e:
                    return await msg.reply_text(
                        text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                return await msg.reply_text(
                    text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply(f'<i>coin kamu ({my_coin}) tidak dapat transfer coin.</i>', True)


@Dk.on_message(filters.private & (filters.text | filters.caption))
async def on_new_menfess(client: Dk, msg: Message):
    if msg.command or msg.text.startswith('/'):
        return await msg.continue_propagation()
    command = msg.text or msg.caption
    pattern = fr"(?:^|\s)({client.hashtag})"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    if command:
        msg.matches = list(regex.finditer(command)) or None
        if not bool(msg.matches):
            await gagal_kirim_handler(client, msg)
            await msg.continue_propagation()
    else:
        await msg.continue_propagation()
    uid = msg.from_user.id
    db = Database(msg.from_user.id, client.me.id)
    if at_check := re.search(r"(?:^|\s)(@[-a-zA-Z0-9@:%._\+~#=]{1,256})", command.lower()):
        try:
            tipe = await client.get_chat(at_check.group(1))
            if tipe.type == enums.ChatType.BOT:
                return await msg.reply('Terdeteksi username bot tidak dapat mengirim menfess')
            elif tipe.type == enums.ChatType.SUPERGROUP:
                return await msg.reply('Terdeteksi username channel/grup tidak dapat mengirim menfess')
            elif tipe.type == enums.ChatType.GROUP:
                return await msg.reply('Terdeteksi username channel/grup tidak dapat mengirim menfess')
            elif tipe.type != msg.from_user.username:
                return await msg.reply('Kata-kata mengandung username, silahkan promote di @onsbase')
        except:
            pass
    if ln_check := re.search(r"(?:^|\s)(t\.me|telegram\.me)\/([-a-zA-Z0-9@:%._\+~#=]{1,256})", command.lower()):
        try:
            tipe = await client.get_chat(ln_check.group(2))
            if tipe.type == enums.ChatType.BOT:
                return await msg.reply('Terdeteksi username bot tidak dapat mengirim menfess')
            elif tipe.type == enums.ChatType.SUPERGROUP:
                return await msg.reply('Terdeteksi username channel/grup tidak dapat mengirim menfess')
            elif tipe.type == enums.ChatType.GROUP:
                return await msg.reply('Terdeteksi username channel/grup tidak dapat mengirim menfess')
            elif tipe.type != msg.from_user.username:
                return await msg.reply('Kata-kata mengandung username, silahkan promote di @onsbase')
        except:
            return await msg.reply('Terdeteksi link channel/grup/tautan tidak dapat mengirim menfess')
    #d = re.search(fr"(?:^|\s)({config.kata_terlarang})", command.lower())
    if is_bad(command.lower()):
        try:
            return await msg.reply('<b>Pesan Gagal Terkirim</b> karena <b>Pesan</b> anda mengandung <b>Kata Terlarang</b>', quote=True)
        except:
            pass
    key = msg.matches[0].group(1)
    hastag = client.hashtag.split('|')
    member = db.get_data_pelanggan()
    if member.status == 'banned':
        return await msg.reply(f'Kamu telah <b>di banned</b>\n\n<u>Alasan:</u> {db.get_data_bot(client.me.id).ban[str(uid)]}\nsilahkan kontak admin @leoopttt untuk unbanned', True, enums.ParseMode.HTML)
    if key in hastag:
        if key == command.lower() or len(command.split(' ')) < 3:
            return await msg.reply('🙅🏻‍♀️  post gagal terkirim, <b>mengirim pesan wajib lebih dari 3 kata.</b>', True, enums.ParseMode.HTML)
        else:
            return await send_menfess_handler(client, msg)
    else:
        await gagal_kirim_handler(client, msg)


async def gagal_kirim_handler(client: Client, msg: Message):
    anu = Helper(client, msg)
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    fullname = first_name if not last_name else first_name + ' ' + last_name
    username = '@leoopttt' if not msg.from_user.username else '@' + msg.from_user.username
    mention = msg.from_user.mention
    hastag = client.hashtag.split("|")
    return await msg.reply(config.gagalkirim_msg.format(
        id=msg.from_user.id,
        mention=mention,
        username=username,
        h1=hastag[0],
        h2=hastag[1],
        h3=hastag[2],
        h4=hastag[3],
        first_name=await anu.escapeHTML(first_name),
        last_name=await anu.escapeHTML(last_name),
        fullname=await anu.escapeHTML(fullname)
    ), True, enums.ParseMode.HTML, disable_web_page_preview=True)