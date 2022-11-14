from subprocess import Popen, PIPE
from truco import Partida

# Crear sala (1v1/2v2/3v3) 1v1

class Gameroom(object):
        owner = ""
        players = []
        name = ""

        def __init__(self, owner, name):
            self.owner = owner
            self.players = [owner]
            self.room_id = id(self)
            self.name = name
            self.state = "Esperando para comenzar"
            self.exp_r = {}

class SuperBot:

    def __init__(self, name):
        self.name = name
        # {0.author.mention}
        self.lock = False
        self.author = ""
        self.args = None
        self.owners = {}
        self.rooms = {}
        self.match = ""
        self.e_reaction = ""
        self.rtable = {}
        print('quetal')


    def handle_message(self, full, author):
        print("Message is:")
        print(full)

        self.args = full.split()
        self.author = author
        cmd = self.args[0]
        self.args = self.args[1:]

        return self.switch(cmd)

    def handle_reaction(self, reaction, author):
        print("Reacted message is:")
        print(reaction.message.content)

        self.author = author
        self.e_reaction = reaction.emoji

        if self.is_he_joined(author):
            current_room = self.room_joined(author)
            if (reaction.emoji, author) in self.rooms[current_room].exp_r:
                return self.r_switch(
                    self.rooms[current_room].exp_r[(reaction.emoji, author)])

    def create_room(self):
        user_id = self.author
        room_name = self.args[0]

        if user_id in self.owners:
            print("rejected - existent owner cannot own another room")
            return """
                Ya eres dueño de la sala {0}, no puedes tener mas de una.
            """.format(self.room_joined(self.author))
        if room_name in self.rooms:
            print("rejected - existent room cannot be created")
            return """
                La sala {0} ya existe y fue creada por {1}. Intenta con otro\
                 nombre
            """.format(room_name, self.rooms[room_name].owner.mention)
            print("ok")

        self.owners[user_id] = room_name
        room = Gameroom(user_id, room_name) 
        self.rooms[room_name] = room
        print(self.rooms)
        return """
            La sala **{0}** ha sido creada.
            Los jugadores presentes son: {1}
            La *id* unica de la sala es: **{2}**
        """.format(room.name, list(map(lambda x : x.mention, room.players)),
        room.room_id)

    def gamerooms(self):
        if len(self.rooms) != 0: 
            roomlist = "Estas son las salas disponibles actualmente:\n "
            for room_name in self.rooms:
                roomlist = "".join((roomlist, 
                    "La sala *{0}*, creada por **{1}**, con **{3}** jugador/es esta {2}.\n"
                    .format(room_name, self.rooms[room_name].owner.mention, 
                        self.rooms[room_name].state, 
                        len(self.rooms[room_name].players))))
            return roomlist
        return 'No hay salas disponibles'

    def exit_room(self):
        for room_name in self.rooms:
            if self.author in self.rooms[room_name].players:
                if self.author is self.rooms[room_name].owner:
                    del(self.rooms[room_name])
                    del(self.owners[self.author])
                    return 'Has salido exitosamente y la sala'\
                     ' {0} ya no existe!'.format(room_name)
                else:
                    self.rooms[room_name].players.remove(self.author)
                    return 'Ya no estas en la sala {0}'.format(room_name)
        return 'No estas en una sala'

    def join(self):
        chosen_room = self.args[0]
        if not self.is_he_joined(self.author):
            if chosen_room in self.rooms:
                if self.author in self.rooms[chosen_room].players:
                    print(self.author)
                    print("\n")
                    print(self.rooms[chosen_room].owner)
                    return 'Ya estas unido a esa sala'
                else:
                    self.rooms[chosen_room].players.append(self.author)
                    return 'Te has unido correctamente a'\
                        ' la sala {0}'.format(chosen_room)
            return 'Esa sala no existe'

    def room_info(self):
        if self.args != []:
            chosen_room = self.args[0]
            print(chosen_room) 
            print(self.rooms[chosen_room].name)
            print(chosen_room in self.rooms)
            if chosen_room in self.rooms:
                return """\n
                La sala **{0}** ha sido creada por {1}.
                Los jugadores presentes son: {2}
                La *id* unica de la sala es: **{3}**.
                Los jugadores estan **{4}**
                """.format(self.rooms[chosen_room].name, 
                    self.rooms[chosen_room].owner.mention, 
                    list(map(lambda x : x.mention, 
                        self.rooms[chosen_room].players)),
                    self.rooms[chosen_room].room_id,
                    self.rooms[chosen_room].state)
            else:
                return "Esa sala no existe. Intentalo de nuevo"
        elif self.is_he_joined(self.author):
            chosen_room = self.room_joined(self.author)
            return """\n
            La sala **{0}** ha sido creada por {1}.
            Los jugadores presentes son: {2}
            La *id* unica de la sala es: **{3}**.
            Los jugadores estan **{4}**
            """.format(self.rooms[chosen_room].name, 
                self.rooms[chosen_room].owner.mention, 
                list(map(lambda x : x.mention, 
                    self.rooms[chosen_room].players)),
                self.rooms[chosen_room].room_id,
                self.rooms[chosen_room].state)
        else:
            print(self.is_he_joined(self.author))
            return "No perteneces a ninguna sala. Por que no intentas unirte a una primero?"

    def is_he_joined(self, player):
        is_he = False
        for room in self.rooms:
            is_he = (is_he) or (self.author in self.rooms[room].players)
        return is_he

    def room_joined(self, player):
        r = ""
        for room in self.rooms:
            if player in self.rooms[room].players:
                r = room 
        return r

    def msg_starting_hand(self, players):
        ret = []
        for player in players:
            ret.append((player, 
                self.match.mostrar_mano(player)))
        print(ret)
        return [1, ret, "Las cartas han sido repartidas."]

    def start(self):
        if self.is_he_joined(self.author): 
            if self.author in self.owners:
                room = self.room_joined(self.author)
                self.rooms[room].state = "En juego"
                self.match = Partida(self.rooms[room].players)
                self.match.iniciar_partida(self.rooms[room].owner)
                return self.msg_starting_hand(self.rooms[room].players)
            else:
                return "No eres el dueño de la sala, espera a que el dueño" \
                " inicie la partida."
        else:
            return "No perteneces a una sala, puedes usar el comando $gamerooms"\
            " para ver las salas disponibles."

    def show_mano(self):
        if self.rooms[self.room_joined(self.author)].state == "En juego":
            return """\n
            Tus cartas son: {0}
            """.format(self.match.mostrar_mano(self.author))

    def pass_turn(self):
        player = self.match.turno()
        room = self.room_joined(player)
        n = 1
        for card in self.match.mano_actual(player):
            if card != 0:
                self.rooms[room].exp_r[("{0}\u20e3".format(n),
             player)] = 'play_turn'
            n = n + 1
        return [2, self.match.mano_actual(player),
        "Es el turno de {0}. Juega una carta".format(player.mention)]

    def play_turn(self):
        reaction_value = {
            "1\u20e3": 0,
            "2\u20e3": 1,
            "3\u20e3": 2
        }
        self.rooms[self.room_joined(self.author)].exp_r = {}
        carta_jugada = self.match.jugar_carta(self.author, reaction_value[self.e_reaction])
        return [3, '{0} ha jugado {1}'.format(self.author.mention, carta_jugada)]

    def who_stays(self, caller, call):

        return """
        {0} ha cantado {1}.\n
        Reacciona acorde a si quieres o no:\n
        """
        # \U0001f44d thumbs up
        # \U0001f44e

    def player_remains(self):
        return  

    def truco(self):
        while self.lock:
            pass
        self.lock = True
        if self.match.get_state()[0] < 1:
            self.match.cantar(1,0)
        return [4, self.who_stays(self.author, 'truco'), self.match.players]        

    def envido(self):
        return

    def switch(self, uInput):
        cmd = {
            'create_room': self.create_room,
            'gamerooms': self.gamerooms,
            'exit_room': self.exit_room,
            'join': self.join,
            'room_info': self.room_info,
            'start': self.start,
            'show_mano': self.show_mano,
            'truco': self.truco,
            'envido': self.envido
        }
        func = cmd.get(uInput)
        return func()

    def r_switch(self, uInput):
        cmd = {
            'play_turn': self.play_turn,
        }
        func = cmd.get(uInput)
        return func()