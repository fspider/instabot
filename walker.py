from controller import Controller
from actor import Actor
import time

class Walker:

    def __init__(self, logger):
        self.logger = logger
        self.savedFilename = "followings.dat"
        self.followings = []
        self.unfollowings = []

        self.actor = Actor()
        self.controller = self.actor.controller
        self.search_delay = self.actor.get_config('main', 'search_delay')
        self.num_followers = self.actor.get_config('main', 'num_followers')

    def start(self):
        self.loadNewFollowingList()
        # self.checkFollowings()
        # self.removeUnfollowings()
        # self.startNewFollowings()
        # self.saveFollowingList()

        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')
        self.controller.mouse_click_name('search')
        self.controller.key_input('spider')

    def loadNewFollowingList(self):
        self.logger.info('-> Loading Data')
        f = open(self.savedFilename, "r")
        for x in f:
            self.followings.append(x[:-1])
        f.close()
        self.logger.info('<- Loading Data')

    def checkFollowings(self):
        self.logger.info('-> Check Following')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('followers')

        new_followings = []
        self.unfollowings = []

        for following in self.followings:
            self.controller.mouse_click_name('search')
            self.controller.key_input(following)
            time.sleep(self.search_delay)

            res = self.actor.capture_search_result()
            if res == True: # Keep
                new_followings.append(following)
                self.logger.info('    ' + following + ' is Following me')
            else : # remove
                self.unfollowings.append(following)
                self.logger.info('    ' + following + ' is not Following me')

            self.controller.mouse_click_name('search')
            self.controller.key_remove(following)
        self.followings = new_followings
        self.controller.mouse_click_name('back')
        self.logger.info('<- Check Following')

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

    def removeUnfollowings(self):
        self.logger.info('-> Remove Followings')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')

        for unfollowing in self.unfollowings:
            self.controller.mouse_click_name('search')
            self.controller.key_input(unfollowing)
            time.sleep(self.search_delay)

            res = self.actor.capture_search_result()
            if res == True: # Keep
                self.actor.unfollow_one(unfollowing)
                self.logger.info('    ' + unfollowing + ' removed')

            else :
                self.followings.append(unfollowing)
                self.logger.info('    ' + unfollowing + ' not removed')

            self.controller.mouse_click_name('search')
            self.controller.key_remove(unfollowing)

        self.controller.mouse_click_name('back')
        self.logger.info('<- Remove Followings')

    def startNewFollowings(self):
        self.logger.info('-> Start Followings')

        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        # self.controller.mouse_click_name('discover_suggested')
        self.controller.item_scroll_prepare()


        for i in range(self.num_followers):
            self.controller.item_scroll_down()
            name = self.actor.follow_one()
            if name != '':
                self.followings.append(name)
                self.logger.info('    ' + 'Adding -> ' + name)

        self.controller.mouse_click_name('back')
        self.logger.info('<- Start Followings')

    def saveFollowingList(self):
        self.logger.info('-> Save Data')
        with open(self.savedFilename, 'w') as f:
            for name in self.followings:
                f.write(name + '\n')
        self.logger.info('<- Save Data')
