from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl import functions as f
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import PeerChannel


class MyTelegram:
    _name = ''
    _api_id = 0
    _api_hash = ''
    _phone_number = ''
    _password = ''
    _client = None
    _dialogs = None

    def __init__(self, name, api_id, api_hash, phone, password):
        self._name = name
        self._api_id = api_id
        self._api_hash = api_hash
        self._phone_number = phone
        self._password = password

        self._client = TelegramClient(self._name, self._api_id, self._api_hash)
        self._client.connect()

        if not self._client.is_user_authorized():
            print('Not authorized')
            self._client.send_code_request(self._phone_number)
            try:
                self._client.sign_in(self._phone_number, input('Enter code:\n'))
            except SessionPasswordNeededError:
                self._client.sign_in(password=self._password)

        if self._client.is_user_authorized():
            print('Authorized')

        self._dialogs = self._client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=1
        ))

    def get_channels_list(self):
        links = set()
        chats = {}
        for c in self._dialogs.chats:
            chats[c.id] = c
        for d in self._dialogs.dialogs:
            peer = d.peer
            if isinstance(peer, PeerChannel):
                id = peer.channel_id
                channel = chats[id]
                if channel.username is not None:
                    link = 'https://t.me/' + str.lower(channel.username)
                    links.add(link)
                    print(link)
        return links

    def leave_all_channels(self):
        chats = {}
        for c in self._dialogs.chats:
            chats[c.id] = c
        for d in self._dialogs.dialogs:
            peer = d.peer
            if isinstance(peer, PeerChannel):
                id = peer.channel_id
                channel = chats[id]
                if channel.username is not None:
                    self._client(f.channels.LeaveChannelRequest(channel))
                    print('Leaved from: @' + channel.username)
