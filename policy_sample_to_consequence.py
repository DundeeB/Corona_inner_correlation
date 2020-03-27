from scipy.stats import bernoulli
import matplotlib.pyplot as plt
from random import randint
import numpy as np

day = 1.0
hour = day / 24
week = 7 * day
minute = hour / 60
second = minute / 60


def infect(people: list, p_external: float, q_internal: float):
    """
    :param people: list of boolian variable of people who are either sick
                    (True - infected) or healthy (False, not infected)
    :param p_external: chance for each healthy person to get sick
    :param q_internal: change of each person to get infected from someone who is sick in the group
    :return: infected people
    """
    n_internal = 0
    n_external = 0
    for i in range(len(people)):
        if people[i] == True:
            for j in range(len(people)):
                if people[j] == False:
                    if bernoulli.rvs(q_internal) == 1:
                        people[j] = True  # person j infected by sick person i
                        n_internal += 1
        else:
            if bernoulli.rvs(p_external) == 1:
                people[i] = True  # person i got infected from outside
                n_external += 1
    return people, n_external, n_internal


def sample(people: list, sampled_indices):
    """
    :param people: list of boolian, true means sick (infected)
    :param n_sample: number of people we sample out of all N. We sample the first N out of people
    :return: True if any of the tested is infected
    """
    for i in sampled_indices:
        if people[i] == True:
            return True
    return False


def single_real(p_dt, q_dt, n_people, dt, tau):
    sample_result = False
    people = n_people * [False]
    # people[randint(0, len(people) - 1)] = True

    sick_people = []
    time = []
    t = 0
    sample_times = 0
    t_first_infected = 0
    last_person_sampled = 0
    n_external = 0
    n_internal = 0
    while sample_result == False:
        t += dt
        time.append(t)
        people, n_external_new, n_internal_new = infect(people, p_dt, q_dt)
        n_internal += n_internal_new
        n_external += n_external_new
        if t_first_infected == 0 and sum(people) > 0:
            t_first_infected = t
        if t >= tau * sample_times:
            sampled_indices = range(last_person_sampled, last_person_sampled + n_sample)
            sampled_indices = [np.mod(n, len(people)) for n in sampled_indices]
            last_person_sampled = sampled_indices[-1]
            sample_result = sample(people, sampled_indices)
            sample_times += 1
        sick_people.append(sum(people))
    t_free = t - t_first_infected
    n_sick_when_identify = sum(people)
    return time, sick_people, t_free, n_sick_when_identify, n_external, n_internal


n_people = 50
n_sample = round(20 / 100 * n_people)
T_external = day/30
p_external = 5.0 / 100 * 0.5 / 100  # 5% of patient are sick and 0.5% chance of infection
T_internal = day/10
q_internal = 0.5/100  # once someone is sick infection has q_T chance per other person to be infected per day
tau = 4 * day
dt = day / 30  # 30 incounters of patient per doc per day
N_real = 10

p_dt = 1 - (1 - p_external) ** (dt / T_external)
q_dt = 1 - (1 - q_internal) ** (dt / T_internal)

t_free, n_sick_final, n_ext, n_int = [], [], [], []
plt.figure(1)
for i in range(N_real):
    t, sick_t, t_sick_free, n_sick_fin, n_external, n_internal = single_real(p_dt, q_dt, n_people, dt, tau)
    t_free.append(t_sick_free)
    n_sick_final.append(n_sick_fin)
    n_ext.append(n_external)
    n_int.append(n_internal)
    plt.plot(t, sick_t, 'b.-')
font = {'size': 22}
plt.xlabel('time [days]', fontdict=font)
plt.ylabel('number of sick people', fontdict=font)
plt.title(str(n_sample) + ' sampled from ' + str(n_people) + \
          ' every ' + str(tau) + ' days', fontdict=font)
plt.rcParams.update({'font.size': 22})
plt.grid()

plt.figure(2)
plt.hist(t_free)
plt.title(str(n_sample) + ' sampled from ' + str(n_people) + \
          ' every ' + str(tau) + ' days')
plt.xlabel('time from first infected until sample is positive [days]')
plt.ylabel('occurence')
plt.rcParams.update({'font.size': 22})

plt.figure(3)
plt.hist(n_sick_final)
plt.title(str(n_sample) + ' sampled from ' + str(n_people) + \
          ' every ' + str(tau) + ' days')
plt.xlabel('number of sick people when sample is positive')
plt.ylabel('occurence')
plt.rcParams.update({'font.size': 22})

plt.figure(4)
plt.hist(n_int)
plt.title(str(n_sample) + ' sampled from ' + str(n_people) + \
          ' every ' + str(tau) + ' days')
plt.xlabel('number of sick people from inner correlation')
plt.ylabel('occurence')
plt.rcParams.update({'font.size': 22})

plt.show()
