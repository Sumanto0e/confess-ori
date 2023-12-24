from pyrogram import Client, enums, types
from menfess.helpers import Database, Helper
from menfess.helpers.decorators import Bot


@Bot("help")
async def on_help_handler(client: Client, msg: types.Message, db: Database):
    member = db.get_data_pelanggan()
    pesan = "Supported commands\n"
    pesan += '/status — melihat status\n'
    pesan += '/topup — top up coin\n'
    pesan += '/tf_coin — transfer coin\n'
    pesan += '/rubahstatus — merubah status\n'
    if member.status == 'admin':
        pesan += '\nHanya Admin\n'
        pesan += '/tf_coin — transfer coin\n'
        pesan += '/settings — melihat settingan bot\n'
        pesan += '/list_admin — melihat list admin\n'
        pesan += '/list_ban — melihat list banned\n\n'
        pesan += 'Perintah banned\n'
        pesan += '/ban — ban user\n'
        pesan += '/unban — unban user\n'
    if member.status == 'owner':
        pesan += '\n=====OWNER COMMAND=====\n'
        pesan += '/tf_coin — transfer coin\n'
        pesan += '/settings — melihat settingan bot\n'
        pesan += '/list_admin — melihat list admin\n'
        pesan += '/list_ban — melihat list banned\n'
        pesan += '/stats — melihat statistik bot\n'
        pesan += '/bot — setbot (on|off)\n'
        pesan += '\n=====FITUR TALENT=====\n'
        pesan += '/addtalent — menambahkan talent baru\n'
        pesan += '/addsugar — menambahkan talent daddy sugar\n'
        pesan += '/addproplayer — menambahkan talent proplayer\n'
        pesan += '/addtemancurhat — menambahkan talent teman curhat\n'
        pesan += '/addgf — menambahkan talent girlfriend rent\n'
        pesan += '/addbf — menambahkan talent boyfriend rent\n'
        pesan += '/addborneo — menambahkan status borneoensis\n'
        pesan += '/addjakartans — menambahkan status jakartans\n'
        pesan += '/addbalinese — menambahkan status balinese\n'
        pesan += '/addpickme — menambahkan status pick me\n'
        pesan += '/addsadgirl — menambahkan status sad girl\n'
        pesan += '/addbabygirl — menambahkan status baby girl\n'
        pesan += '/addabg — menambahkan status abg\n'
        pesan += '/addmelayu — menambahkan status melayu\n'
        pesan += '/addwongjowo — menambahkan status wong jowo\n'
        pesan += '/addbodygoals — menambahkan status bodygoals\n'
        pesan += '/hapus — menghapus talent\n'
        pesan += '\n=====BROADCAST OWNER=====\n'
        pesan += '/broadcast — mengirim pesan broadcast kesemua user\n'
        pesan += '/admin — menambahkan admin baru\n'
        pesan += '/unadmin — menghapus admin\n'
        pesan += '/member — penguna dijadikan member\n'
        pesan += '/unmember — penguna dijadikan unmember\n'
        pesan += '/list_ban — melihat list banned\n'
        pesan += '\n=====BANNED COMMAND=====\n'
        pesan += '/ban — ban user\n'
        pesan += '/unban — unban user\n'
    await msg.reply(pesan, True)