import inquirer
import numpy as np
import pandas as pd


class Member:
    def __init__(self, full_name, age, height, weight):
        self.full_name = full_name
        self.age = age
        self.height = height
        self.weight = weight
        self.calculate_bmi()

    def calculate_bmi(self):
        bmi = self.weight / (self.height/100)**2
        if bmi < 18.5:
            category = 'Underweight'
        elif bmi > 18.5 and bmi < 24.9:
            category = 'Normal weight'
        elif bmi > 25 and bmi < 29.9:
            category = 'Overweight'
        elif bmi > 30:
            category = 'Obesity'

        self.bmi = bmi
        self.category = category

    def info(self):
        print(self.full_name, 'is', str(self.age),
              'years old and is', str(self.height), 'cm.')

    def info_detailed(self):
        print(self.full_name, 'is', str(self.age), 'years old.')
        print('Height:', str(self.height))
        print('Weight:', str(self.weight))
        print('BMI:', str(format(self.bmi, ".2f")), '-->', self.category)
        print('---------------------------')


class Gym:
    def __init__(self):
        self.members = np.array([])
        self.members_info = np.array([])
        self.hakans = np.array([])

    def add_member(self, full_name, age, height, weight):

        member = Member(full_name, age, height, weight)

        if 'hakan' in full_name:
            member.full_name = member.full_name.replace('hakan', 'hasan')
            member.weight = weight + 5
            self.hakans = np.append(self.hakans, member)

        self.members = np.append(self.members, member)

        self.sort_members()
        self.fetch_members_info()

    def remove_member(self, member):
        i,  = np.where(self.members == member)
        self.members = np.delete(self.members, i[0])

        if member in self.hakans:
            i,  = np.where(self.hakans == member)
            self.hakans = np.delete(self.hakans, i[0])

        self.sort_members()
        self.fetch_members_info()

    def edit_member(self, member, age, height, weight):
        member.age = age
        member.height = height
        member.weight = weight
        member.calculate_bmi()

        self.sort_members()
        self.fetch_members_info()

    def show_members_info(self):
        if self.members.size == 0:
            print('There are no members!')
        else:
            for member in self.members:
                member.info()

    def show_members_info_detailed(self):
        if self.members.size == 0:
            print('There are no members!')
        else:
            for member in self.members:
                member.info_detailed()

    def sort_members(self):
        copy = self.members.tolist()
        copy.sort(key=lambda x: x.age)
        self.members = np.array(copy)
        if self.hakans.size != 0:
            for i in range(self.hakans.size):
                ihakan, = np.where(self.members==self.hakans[i])
                self.members = np.delete(self.members, ihakan[0])
                self.members = np.append(self.members, self.hakans[i])

    def get_member(self, index):
        return self.members[index]

    def fetch_members_info(self):
        self.members_info = np.array([])
        for member in self.members:
            self.members_info = np.append(self.members_info, member.full_name + ' is ' + str(member.age) +
                                          ' years old and is ' + str(member.height) + ' cm.')

    def import_members(self):
        members_df = pd.read_excel('./members.xlsx', index_col=0,)

        # members = members.loc([1,-1])

        members = members_df.to_numpy()

        for member in members:
            try:
                full_name = member[0]
                age = int(member[1])
                height = float(member[2])
                weight = float(member[3])

                self.add_member(full_name, age, height, weight)

                print('Member added.')

            except ValueError:
                print('Please provide right member info')

    def export_members(self):
        if (self.members.size == 0):
            print('There is no members')
            return

        names = np.array([])
        ages = np.array([])
        heights = np.array([])
        weights = np.array([])
        bmis = np.array([])
        categories = np.array([])
        for member in self.members:
            if (member in self.hakans):
                member.full_name.replace('hasan', 'hakan')
            names = np.append(names, member.full_name)
            ages = np.append(ages, member.age)
            heights = np.append(heights, member.height)
            weights = np.append(weights, member.weight)
            bmis = np.append(bmis, format(member.bmi, ".2f"))
            categories = np.append(categories, member.category)

        members = pd.DataFrame({
            'Name': names,
            'Age': ages,
            'Height': heights,
            'weight': weights,
            'Body Mass Index': bmis,
            'Category': categories,
        })

        writer = pd.ExcelWriter('./members.xlsx')
        members.to_excel(writer)
        members.to_excel(writer, 'Members')
        writer.save()

    def reset(self):
        self.members = np.array([])
        self.members_info = np.array([])
        self.hakans = np.array([])


def get_member_from_user(gym):
    members = [
        inquirer.List(
            'member',
            message="Please select the member to remove",
            choices= gym.members_info.tolist(),
        ),
    ]
    member_i = inquirer.prompt(members)["member"]

    member_index,  = np.where(gym.members_info==member_i)

    print(member_index)

    return gym.get_member(member_index[0])


def confirm_user():
    confirm = {
        inquirer.Confirm(
            'confirm',
            message="Are you sure?",
            default=True
        ),
    }
    return inquirer.prompt(confirm)['confirm']


def do_action(action_number):
    if action_number == 0:
        print(actions[0])
        member_info = [
            inquirer.Text('name', message="What's member's name"),
            inquirer.Text('surname', message="What's member's surname"),
            inquirer.Text('age', message="What's member's age"),
            inquirer.Text('height', message="What's member's height in cm"),
            inquirer.Text('weight', message="What's member's weight in kg"),
        ]
        answers = inquirer.prompt(member_info)

        try:
            age = int(answers['age'])
            height = float(answers['height'])
            weight = float(answers['weight'])

            gym.add_member(answers['name'],
                           answers['surname'], age, height, weight)

            print('Member added.')

        except ValueError:
            print('Please provide right member info')

    elif action_number == 1:
        print(actions[1])

        member_to_remove = get_member_from_user(gym)

        member_to_remove.info_detailed()

        if confirm_user():
            gym.remove_member(member_to_remove)

            print('Member removed.')

            gym.show_members_info()
            print('---------------------------')

    elif action_number == 2:
        print(actions[2])

        member_to_edit = get_member_from_user(gym)

        member_info = [
            inquirer.Text('age', message="What's member's age"),
            inquirer.Text('height', message="What's member's height in cm"),
            inquirer.Text('weight', message="What's member's weight in kg"),
        ]
        answers = inquirer.prompt(member_info)

        try:
            age = int(answers['age'])
            height = float(answers['height'])
            weight = float(answers['weight'])

            gym.edit_member(member_to_edit, age, height, weight)
            member_to_edit.info_detailed()
            print('---------------------------')

            print('Member edited.')
        except ValueError:
            print('Please provide right member info')

    elif action_number == 3:
        print(actions[3])

        is_detailed_list = ['Normal', 'Detailed']

        is_detailed = [
            inquirer.List(
                'is_detailed',
                message="Please select the member to remove",
                choices=is_detailed_list,
            ),
        ]
        is_detailed_sel = inquirer.prompt(is_detailed)["is_detailed"]

        if is_detailed_list.index(is_detailed_sel) == 0:
            gym.show_members_info()
            print('---------------------------')
        else:
            gym.show_members_info_detailed()

    elif action_number == 4:
        print(actions[4])
        gym.import_members()

    elif action_number == 5:
        print(actions[5])
        gym.export_members()
        
    elif action_number == 6:
        print(actions[6])
        gym.reset()
    elif action_number == 7:
        print(actions[7])
        exit()


if __name__ == "__main__":
    gym = Gym()

    gym.add_member('ert sa', 23, 188, 108)
    gym.add_member('eren oz', 22, 175, 70)
    gym.add_member('berkant fa', 24, 180, 85)
    gym.add_member('hakan ha', 19, 205, 130)

    actions = [
        'Add member',
        'Remove member',
        'Edit member',
        'Show members',
        'Import excel',
        'Export excel',
        'Reset',
        'Exit',
    ]

    while True:
        questions = [
            inquirer.List(
                'action',
                message="Welcome! Please select",
                choices=actions,
            ),
        ]
        action = inquirer.prompt(questions)["action"]
        action_number = actions.index(action)

        do_action(action_number)
