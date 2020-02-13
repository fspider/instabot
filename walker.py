from controller import Controller
from actor import Actor
import time

class Walker:

    def __init__(self):
        self.savedFilename = "followings.dat"
        self.followings = []

        self.actor = Actor()
        self.controller = self.actor.controller

    def start(self):
        self.loadNewFollowingList()
        self.checkFollowings()
        # self.startNewFollowings()
        # self.saveFollowingList()
        # res = self.actor.capture_search_result()

    def loadNewFollowingList(self):
        f = open(self.savedFilename, "r")
        for x in f:
            self.followings.append(x[:-1])
        f.close()

    def checkFollowings(self):
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('followers')
        self.controller.mouse_click_name('search')
        for following in self.followings:
            self.controller.mouse_click_name('search')
            self.controller.key_input(following)
            res = self.actor.capture_search_result()
            if res == False:
                # remove
            self.controller.mouse_click_name('search')
            self.controller.key_remove(following)

    def test():
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')
        self.controller.mouse_click_name('discover_suggested')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('followers')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('following')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('search')
        self.controller.mouse_click_name('discover_plus')

    def removeUnFollowings(self):
        pass

    def startNewFollowings(self):
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        # self.controller.mouse_click_name('discover_suggested')
        self.controller.item_scroll_prepare()

        self.num_follows = self.actor.get_config('main', 'num_followers')

        for i in range(self.num_followers):
            self.controller.item_scroll_down()
            name = self.actor.follow_one()
            if name != '':
                self.followings.append(name)
                print('Adding -> ', name)

        self.controller.mouse_click_name('back')

    def saveFollowingList(self):
        print('start saving followings to file')
        with open(self.savedFilename, 'w') as f:
            for name in self.followings:
                f.write(name + '\n')
        print('completed saving to file')
