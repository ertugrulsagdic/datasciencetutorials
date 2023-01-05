import inquirer


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
        self.members = []
        self.members_info = []
        self.hakans = []

    def add_member(self, name, surname, age, heigth, weigth):

        member = Member((name + ' ' + surname), age, heigth, weigth)

        if name.lower() == 'hakan':
            member.full_name = ('hasan' + ' ' + surname)
            member.weight = weigth + 5
            self.hakans.append(member)

        self.members.append(member)

        self.sort_members()
        self.fetch_members_info()

    def remove_member(self, member):
        self.members.remove(member)

        if member in self.hakans:
            self.hakans.remove(member)

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
        for member in self.members:
            member.info()

    def show_members_info_detailed(self):
        for member in self.members:
            member.info_detailed()

    def sort_members(self):
        self.members.sort(key=lambda x: x.age)
        if len(self.hakans) != 0:
            for hakan in self.hakans:
                self.members.append(self.members.pop(self.members.index(hakan)))

    def get_member(self, index):
        return self.members[index]

    def fetch_members_info(self):
        self.members_info = []
        for member in self.members:
            self.members_info.append(member.full_name + ' is ' + str(member.age) +
              ' years old and is ' + str(member.height) + ' cm.')


def get_member_from_user(gym):
    members = [
        inquirer.List(
            'member',
            message="Please select the member to remove",
            choices= gym.members_info,
        ),
    ]
    member_i = inquirer.prompt(members)["member"]

    member_index = gym.members_info.index(member_i)

    return gym.get_member(member_index)

def confirm_user():
    confirm = {
            inquirer.Confirm(
                'confirm',
                message="Are you sure?" ,
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
            inquirer.Text('weight', message="What's member's weigth in kg"),
        ]
        answers = inquirer.prompt(member_info)


        try:
            age = int(answers['age']) 
            heigth = float(answers['height'])
            weigth = float(answers['weight'])
            
            gym.add_member(answers['name'], answers['surname'], age, heigth, weigth)

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
            inquirer.Text('weight', message="What's member's weigth in kg"),
        ]
        answers = inquirer.prompt(member_info)

        try:
            age = int(answers['age']) 
            heigth = float(answers['height'])
            weigth = float(answers['weight'])

            gym.edit_member(member_to_edit, age, heigth, weigth)
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
                choices= is_detailed_list,
            ),
        ]
        is_detailed_sel = inquirer.prompt(is_detailed)["is_detailed"]
        
        if is_detailed_list.index(is_detailed_sel) == 0:
            gym.show_members_info()
            print('---------------------------')
        else:
            gym.show_members_info_detailed()

    elif action_number == 4:
        exit()

if __name__ == "__main__":
    gym = Gym()

    gym.add_member('ert', 'sa', 23, 188, 108)
    gym.add_member('eren', 'oz', 22, 175, 70)
    gym.add_member('berkant', 'fa', 24, 180, 85)
    gym.add_member('hakan', 'ha', 19, 205, 130)

    actions = ['Add member', 'Remove member', 'Edit member', 'Show members', 'Exit']

    while True:
        questions = [
            inquirer.List(
                'action',
                message="Welcome! Please select",
                choices= actions,
            ),
        ]
        action = inquirer.prompt(questions)["action"]
        action_number = actions.index(action)

        do_action(action_number)
