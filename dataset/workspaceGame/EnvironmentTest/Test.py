import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.Game.Environment import BJEnvironment
env = BJEnvironment()


def print_obs(obs):
    print("Cartas Jugador", obs[0][0])
    print("Cartas Dealer", obs[0][1])
    print("Un usuario tiene ace", bool(obs[0][2]))
    print("El jugador tiene split", bool(obs[0][3]))
    print("El jugador tiene double", bool(obs[0][4]))
    print(f"El jugador le falta {obs[0][5]*10}% de bolar en 21")
    print("Estado de juego", obs[0][6])

count = 1
while True:
    print(count)
    done = False
    env.reset(5)
    while not done:

        obs = env.get_obs()
        print_obs(obs)

        action = int(input("Ingrese su accion: 1:Hit, 2:Stand, 3:Double, 4:Split:"))
        action = action - 1
        state, action, reward, next_state, done = env.step(action)

        if done == 1:
            print_obs(next_state)
            if reward > 0:
                print("Gano")
            if reward == 0:
                print("Empato")
            if reward < 0:
                print("Perdio")
    input()
    count = count + 1
