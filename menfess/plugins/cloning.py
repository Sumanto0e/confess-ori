import asyncio
import traceback

from menfess.database.clone_db import Owner
from menfess.dk import Dk
from menfess.helpers import Database, Helper, isUser, isAdmin
from menfess.helpers.decorators import Bot
import config
import re
from pyrogram import filters
from pyromod import Client, Message
from pyromod.exceptions.listener_timeout import ListenerTimeout
from menfess import bots, dbclone, Clone

from pyrogram.errors import ChannelInvalid


@Bot("clone")
async def on_clone_handler(client: Client, msg: Message, db: Database = None):
    if client.owner_id != 0:
        return await msg.reply("❌ <b>ERROR</b>\n\n<b>Bot ini sudah melakukan clone</b>")
    who = msg.from_user
    isuser = await isUser(who.id)
    if isuser is not True:
        return await msg.reply_text(
            isuser)
    m = await msg.reply("🔄 <b>Clonning...</b>")
    try:
        user = Clone(who.id)
        already_clone = await user.get_clone()
        if already_clone is not None:
            if not already_clone.status:
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Anda sudah melakukan clone</b>, tetapi anda sudah dibanned")
            return await m.edit("❌ <b>ERROR</b>\n\n<b>Anda sudah melakukan clone</b>, /settings untuk melihat detail "
                                "clone")
        try:
            ask = await m.chat.ask(
                "Silahkan Kirim kan BOT TOKEN yang didapat dari @BotFather\n <b>PASTIKAN BOT SUDAH MASUK KE FSUB GROUP, CHANNEL, DATABASE dan Sebagai ADMIN</b>, JIKA BELUM SILAHKAN MASUKAN DAN JADIKAN ADMIN LALU KIRIM KAN TOKEN NYA\n/cancel untuk membatalkan",
                timeout=600)
            if ask.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask.sent_message.id, ask.id])
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Proses Dibatalkan</b>")
            token = ask.text
            ask_ch1 = await m.chat.ask(
                "Silahkan Kirim kan ID CHANNEL 1 yang akan dijadikan CHANNEL 1\n,Perlu diperhatikan untuk mengirim ID dengan benar\n/cancel untuk membatalkan",
                timeout=300)
            if ask_ch1.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask_ch1.sent_message.id, ask_ch1.id])
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Proses Dibatalkan</b>")
            elif "-100" not in ask_ch1.text:
                return await m.edit(
                    "❌ <b>ERROR</b>\n\n<b>ID CHANNEL 1</b>\nContoh yang benar diawali dengan -100, misalnya -1001234567890")

            ask_ch2 = await m.chat.ask(
                "Silahkan Kirim kan ID CHANNEL 2 yang akan dijadikan CHANNEL 2\n,Perlu diperhatikan untuk mengirim ID dengan benar\n/cancel untuk membatalkan",
                timeout=300)
            if ask_ch2.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask_ch2.sent_message.id, ask_ch2.id])
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Proses Dibatalkan</b>")
            elif "-100" not in ask_ch2.text:
                return await m.edit(
                    "❌ <b>ERROR</b>\n\n<b>ID CHANNEL 2</b>\nContoh yang benar diawali dengan -100, misalnya -1001234567890")


            ask_ch_tf = await m.chat.ask(
                "Silahkan Kirim kan ID CHANNEL TF yang akan dijadikan CHANNEL TF\n,Perlu diperhatikan untuk mengirim ID dengan benar\n/cancel untuk membatalkan",
                timeout=300)
            if ask_ch_tf.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask_ch_tf.sent_message.id, ask_ch_tf.id])
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Proses Dibatalkan</b>")
            elif "-100" not in ask_ch_tf.text:
                return await m.edit(
                    "❌ <b>ERROR</b>\n\n<b>ID CHANNEL TF</b>\nContoh yang benar diawali dengan -100, misalnya -1001234567890")


            ask_ch_log = await m.chat.ask(
                "Silahkan Kirim kan ID CHANNEL LOG yang akan dijadikan LOG\n,Perlu diperhatikan untuk mengirim ID dengan benar\n/cancel untuk membatalkan",
                timeout=300)
            if ask_ch_log.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask_ch_log.sent_message.id, ask_ch_log.id])
                return await m.edit("❌ <b>ERROR</b>\n\n<b>Proses Dibatalkan</b>")
            elif "-100" not in ask_ch_log.text:
                return await m.edit(
                    "❌ <b>ERROR</b>\n\n<b>ID CHANNEL LOG</b>\nContoh yang benar diawali dengan -100, misalnya -1001234567890")


            ask_hashtag = await m.chat.ask(
                "Silahkan Kirim kan HASHTAG yang akan dijadikan HASHTAG\n,Perlu diperhatikan untuk mengirim ID dengan benar\n/cancel untuk membatalkan",
                timeout=300)
            if ask_hashtag.text == "/cancel":
                await client.delete_messages(m.chat.id, [ask_hashtag.sent_message.id, ask_hashtag.id])
            hashtag = ask_hashtag.text
        except ListenerTimeout:
            return await m.edit("❌ <b>ERROR</b>\n\n<b>Waktu habis, silahkan coba lagi</b>")
        except BaseException:
            return await m.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")

        try:
            ch_1 = int(ask_ch1.text)
            ch_2 = int(ask_ch2.text)
            ch_tf = int(ask_ch_tf.text)
            ch_log = int(ask_ch_log.text)
        except ValueError:
            return await m.reply_text(
                "❌ <b>ERROR</b>\n\n<b>CHANNEL 1, CHANNEL 2, CHANNEL TF, CHANNEL LOG SALAH</b>\nContoh yang benar diawali dengan -100, misalnya -1001234567890")
        except Exception as e:
            print(e)
            return await m.reply_text(f"❌ <b>ERROR</b>\n\n<b>{e}</b>")
        try:
            owner = Owner(
                user_id=who.id,
                username=who.username,
                channel_1=ch_1,
                channel_2=ch_2,
                channel_tf=ch_tf,
                channel_log=ch_log,
                hashtag=hashtag,
                token=token,
                status=True
            )
            try:
                await client.delete_messages(m.chat.id, [
                    ask.sent_message.id, ask.id, ask_ch1.sent_message.id, ask_ch1.id, ask_ch2.sent_message.id, ask_ch2.id,
                    ask_ch_tf.sent_message.id, ask_ch_tf.id, ask_ch_log.sent_message.id, ask_ch_log.id, ask_hashtag.sent_message.id,
                    ask_hashtag.id,
                ])
            except Exception as e:
                print(e)
            clone_stat = await m.edit("🔄 <b>Start Clonning...</b>")
            result, jieh = await Dk(who.id, token, memory=True, owner=owner).start()
            if not result:
                return await clone_stat.edit(f"❌ <b>ERROR</b>\n\n<b>{jieh}</b>")
            if isinstance(jieh, str):
                return await clone_stat.edit(f"❌ <b>ERROR</b>\n\n<b>{jieh}</b>")
            elif isinstance(jieh, Dk):
                add = await user.add_clone(jieh.owner)
                if not add:
                    await jieh.stop()
                    return await clone_stat.edit("❌ <b>ERROR</b>\n\n<b>Gagal Clonning</b>")
            else:
                return await clone_stat.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")
            bots.append(jieh)
            await clone_stat.edit(f"✅ <b>Clone Berhasil</b>\n\n<b>Bot Name:</b> <code>{jieh.me.first_name}</code>\n<b>Bot Username: @{jieh.username}</b>\n Owner: {who.mention}")
        except ChannelInvalid:
            return await m.edit("❌ <b>ERROR</b>\n\n<b>Pastikan bot sudah join didalam group/database</b>")
        except BaseException as e:
            print(e)
            return await m.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")
    except (TimeoutError, ListenerTimeout):
        return await m.edit("❌ <b>ERROR</b>\n\n<b>Waktu habis, silahkan coba lagi</b>")
    except BaseException as e:
        e = traceback.format_exc()
        print(e)
        return await m.edit("❌ <b>ERROR</b>\n\n<b>Terjadi Kesalahan</b>")


@Dk.on_message(filters.command("disable") & isAdmin)
async def on_disable(client: Bot, message: Message):
    global bots
    if client.owner_id != 0:
        for bot in bots:
            try:
                if int(bot.owner_id) == int(client.owner_id):
                    bots.remove(bot)
                    asyncio.create_task(bot.stop())
            except BaseException as e:
                print("disable", e)
                pass
        clone = Clone(client.owner_id)
        await clone.takedown()
    else:
        return await message.reply("❌ <b>ERROR</b>\n\n<b>Tidak bisa mematinkan bot utama</b>", quote=True)


@Dk.on_message(filters.command("listclone") & filters.user(config.id_admin))
async def on_listClone(client: Bot, message: Message):
    clones = await Clone(message.from_user.id).full_clone()
    if len(clones) == 0:
        return await message.reply("❌ <b>Tidak Ada Clone</b>", quote=True)
    text = "📝 <b>Daftar Clone</b> :\n\n"
    for clone in clones:
        if clone.status:
            text += f"🔹 <b>Clone</b> : <code>{clone.user_id}</code> @{clone.username} | <b>Status</b> : <b>Aktif</b>\n"
        else:
            text += f"🔹 <b>Clone</b> : <code>{clone.user_id}</code> @{clone.username} | <b>Status</b> : <b>Banned</b>\n"
    await message.reply(text, quote=True)
