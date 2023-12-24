import config
import re
import random
from pyrogram import Client, enums, types

from menfess.dk import Dk
from menfess.helpers import Database, Helper
from menfess.helpers.decorators import Bot
from config import daget, claimed


@Bot("daget")
async def on_daget_handler(client: Dk, msg: types.Message, database: Database = None):
    global daget, claimed
    try:
        who = msg.from_user
        db = database
        user = db.get_data_pelanggan()
        current_coin = user.coin
        cmd = msg.text.split()
        if len(cmd) < 3:
            return await msg.reply_text("Format salah, `/daget jumlahkoin text`")
        total_daget = int(cmd[1])
        pesan = " ".join(cmd[2:])
        if current_coin < total_daget:
            return await msg.reply_text(f"Koin kamu tidak mencukupi, sisa koin kamu {current_coin}")
        daget = int(daget + total_daget)
        claimed = []
        new_coin = current_coin - total_daget
        gambar = "https://t.me/asdasdadaw2/78"
        entities = msg.entities or msg.caption_entities
        await db.update_coin(new_coin)
        kirim = await client.send_photo(client.channel_1, gambar, f"KOIN KAGET\n\n{pesan}\n\nDari: {msg.from_user.username}\nTotal coin: {total_daget}\n\nAYO BURUAN /claim", caption_entities=entities)
        return await msg.reply_text("Berhasil mengirimkan daget ke channel, koin kamu sudah dipotong sesuai jumlah daget")
    except ValueError:
        return await msg.reply_text("Jumlah koin harus angka")
    except Exception:
        return await msg.reply_text("Gagal mengirimkan daget")


@Bot("claim")
async def on_daget_claim_handler(client: Client, msg: types.Message, database: Database = None):
    global daget, claimed
    who = msg.from_user
    helper = Helper(client, msg)
    if not await database.cek_user_didatabase():
        return await msg.reply_text("Kamu tidak bisa mengikuti daget ini, silahkan daftar dulu ke bot")
    # Pesan jika bot sedang dalam kondisi tidak aktif
    if not database.get_data_bot(client.me.id).bot_status:
        status = [
            'non member', 'member', 'banned', 'talent', 'daddy sugar', 'teman curhat',
            'proplayer', 'girlfriend rent', 'boyfriend rent', 'jakartans', 'balinese',
            'borneoensis', 'melayu', 'sad girl', 'body goals', 'wong jowo', 'abg', 'baby girl', 'pick me'
        ]

        member = database.get_data_pelanggan()
        if member.status in status:
            return await msg.reply_text(text="<i>Saat ini bot sedang dinonaktifkan</i>", parse_mode=enums.ParseMode.HTML)
    try:
        if daget <= 0:
            return await msg.reply_text("Maaf kamu kurang beruntung:(")
        if msg.from_user.id in claimed:
            return await msg.reply_text("Maaf kamu sudah, next time lagi")
        jumlah_dapat = random.randint(1, daget)
        db = Database(msg.from_user.id, client.me.id)
        user = db.get_data_pelanggan()
        current_coin = user.coin
        new_coin = current_coin + jumlah_dapat
        daget = int(daget - jumlah_dapat)
        claimed.append(msg.from_user.id)
        await db.update_coin(new_coin)
        await msg.reply_text(f"Selamat kamu medapatkan {jumlah_dapat} koin yey!")
    except Exception as e:
        print("error:", e)
        pass
