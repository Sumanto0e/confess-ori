from pyrogram import Client, enums, types
from menfess.helpers import Database, Helper
from menfess.helpers.decorators import Bot
import config
import re
from pyrogram import Client, enums, types

@Bot("bfrent")
async def on_bf_rent_handler(client: Client, msg: types.Message, db: Database = None):
    bf_rent = db.get_data_bot(client.me.id).bfrent
    top_rate = [] # total rate bf_rent
    top_id = [] # id bf_rent
    if len(bf_rent) == 0:
        return await msg.reply('<b>Saat ini tidak ada Bf rent yang tersedia.</b>', True, enums.ParseMode.HTML)
    else:
        for uid in bf_rent:
            rate = bf_rent[str(uid)]['rate']
            if rate >= 0:
                top_rate.append(rate)
                top_id.append(uid)
        top_rate.sort(reverse=True)
        pesan = "<b>Daftar Bf rent trusted</b>\n\n"
        pesan += "No — Bf rent — Rating\n"
        index = 1
        for i in top_rate:
            if index > config.batas_bfrent:
                break
            for j in top_id:
                if bf_rent[j]['rate'] == i:
                    pesan += f"<b> {str(index)}.</b> {bf_rent[j]['username']} ➜ {str(bf_rent[j]['rate'])} 👓\n"
                    top_id.remove(j)
                    index += 1
        pesan += f"\nmenampilkan Real BF Rent ONS"
        await msg.reply(pesan, True, enums.ParseMode.HTML)

@Bot(r"^[\/]addbf(\s|\n)*(\d+)$", regex=True)
async def on_add_bf_rent_handler(client: Client, msg: types.Message, db: Database = None):
    helper = Helper(client, msg)
    # if re.search(r"^[\/]addbf(\s|\n)*$", msg.text or msg.caption):
    #     return await msg.reply_text(
    #         text="<b>Cara penggunaan tambah Bf rent</b>\n\n<code>/addbf id_user</code>\n\nContoh :\n<code>/addbf 121212021</code>", quote=True,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    target = msg.matches[0].group(2)
    db = Database(int(target), client.me.id)
    if target in db.get_data_bot(client.me.id).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan boyfriend rent", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if await db.cek_user_didatabase():
        status = [
            'admin', 'owner', 'talent', 'daddy sugar', 'proplayer',
            'teman curhat', 'girlfriend rent', 'boyfriend rent'
        ]
        member = db.get_data_pelanggan()
        if member.status in status:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Boyfriend rent</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        try:
            a = await client.get_chat(target)
            nama = await helper.escapeHTML(a.first_name if not a.last_name else a.first_name + ' ' + a.last_name)
            await client.send_message(
                int(target),
                text=f"<i>Kamu telah menjadi Boyfriend rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                parse_mode=enums.ParseMode.HTML
            )
            await db.tambah_bf_rent(int(target), client.me.id, nama)
            return await msg.reply_text(
                text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi Bf rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
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


@Bot("gfrent")
async def on_gf_rent_handler(client: Client, msg: types.Message, db: Database = None):
    gf_rent = db.get_data_bot(client.me.id).gfrent
    top_rate = [] # total rate gf_rent
    top_id = [] # id gf_rent
    if len(gf_rent) == 0:
        return await msg.reply('<b>Saat ini tidak ada Gf rent yang tersedia.</b>', True, enums.ParseMode.HTML)
    else:
        for uid in gf_rent:
            rate = gf_rent[str(uid)]['rate']
            if rate >= 0:
                top_rate.append(rate)
                top_id.append(uid)
        top_rate.sort(reverse=True)
        pesan = "<b>Daftar Gf rent trusted</b>\n\n"
        pesan += "No — Gf rent — Rating\n"
        index = 1
        for i in top_rate:
            if index > config.batas_gfrent:
                break
            for j in top_id:
                if gf_rent[j]['rate'] == i:
                    pesan += f"<b> {str(index)}.</b> {gf_rent[j]['username']} ➜ {str(gf_rent[j]['rate'])} 🌸\n"
                    top_id.remove(j)
                    index += 1
        pesan += f"\nmenampilkan Real GF rent ONS"
        await msg.reply(pesan, True, enums.ParseMode.HTML)


@Bot(r"^[\/]addgf(\s|\n)*(\d+)$", regex=True)
async def om_add_gf_rent_handler(client: Client, msg: types.Message, db: Database = None):
    helper = Helper(client, msg)
    # if re.search(r"^[\/]addgf(\s|\n)*$", msg.text or msg.caption):
    #     return await msg.reply_text(
    #         text="<b>Cara penggunaan tambah Gf rent</b>\n\n<code>/addgf id_user</code>\n\nContoh :\n<code>/addgf 121212021</code>", quote=True,
    #         parse_mode=enums.ParseMode.HTML
    #     )
    target = msg.matches[0].group(2)
    db = Database(int(target), client.me.id)
    if target in db.get_data_bot(client.me.id).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan girlfriend rent", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if await db.cek_user_didatabase():
        status = [
            'admin', 'owner', 'talent', 'daddy sugar', 'prolpayer',
            'teman curhat', 'girlfriend rent', 'boyfriend rent'
        ]
        member = db.get_data_pelanggan()
        if member.status in status:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Girlfriend rent</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        try:
            a = await client.get_chat(target)
            nama = await helper.escapeHTML(a.first_name if not a.last_name else a.first_name + ' ' + a.last_name)
            await client.send_message(
                int(target),
                text=f"<i>Kamu telah menjadi Girlfriend rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                parse_mode=enums.ParseMode.HTML
            )
            await db.tambah_gf_rent(int(target), client.me.id, nama)
            return await msg.reply_text(
                text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi Gf rent</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
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