from controller import Controller
from actor import Actor
import time
import threading
from datetime import datetime, timedelta
import random

random.seed(1)

class WalkerThread(threading.Thread):
    def __init__(self, logger, parent, method, name='WalkerThread'):
        # super(WalkerThread, self).__init__()
        self.parent = parent
        self.method = method

        self._stopevent = threading.Event()
        self._isrunning = threading.Event()
        self._isPausedFollowing = threading.Event()

        self.likesDelaySt = int(self.parent.enLikesDelaySt.get())
        self.likesDelayEd = int(self.parent.enLikesDelayEd.get())

        threading.Thread.__init__(self, name=name)
        self.logger = logger
        self.walker = Walker(parent, self.logger, self._stopevent, self._isPausedFollowing)
    def run(self):
        self._isrunning.set()
        cnt = 0
        self.logger.error('Bot Thread Started!')
        self._stopevent.clear()

        if not self.walker.init():
            self.logger.error('Bot Thread Stopped Automatically!')
            return

        while True:
            cnt = cnt + 1
            self.cycleSt = float(self.parent.enCycleSt.get())
            self.cycleEd = float(self.parent.enCycleEd.get())
            cycle = random.uniform(self.cycleSt, self.cycleEd)

            ed = datetime.now() + timedelta(hours=cycle)
            self.logger.error('[START ' + str(cnt) + 'th Cycle]')

            if self.method == "NORMAL":
                # Finish Last check and Break
                if self.walker.readAll is True:
                    self.walker.start()
                    self.logger.error('All check finished!')
                    break

                self.walker.start()
            elif self.method == "ONLY_UNFOLLOW":
                if self.walker.readAll is True:
                    self.logger.error('All was Unfollowed!')
                self.walker.onlyUnfollow()

            if self._stopevent.isSet():
                break

            self.logger.warning('On idle time until ' + str(ed))
            while datetime.now() < ed:
                if self._stopevent.isSet():
                    break
                time.sleep(3)
                if self.parent.doLikes.get() == 1:
                    self.likes_delay = int(random.uniform(self.likesDelaySt, self.likesDelayEd))
                    self.walker.actor.find_click('likes', self.likes_delay)

            if self._stopevent.isSet():
                break

        self.walker.destory()
        self._isrunning.clear()
        self.logger.error('Bot Thread Ended!')



    def stop(self, timeout=None):
        self._stopevent.set()

    def stopped(self):
        return self._stopevent.is_set()    


class Walker:

    def __init__(self, parent, logger, _stopevent, _isPausedFollowing):
        self.parent = parent
        self.logger = logger
        self._stopevent = _stopevent
        self._isPausedFollowing = _isPausedFollowing

        self.savedFilename = "followings.dat"
        self.savedFollowers = "followers.dat"

        self.actor = Actor(_stopevent, self.parent.setStatus, self.parent)
        self.controller = self.actor.controller
        self.readAll = False

        f = open(self.savedFollowers, 'w+')
        f.close

    def init(self):
        self.followings = []
        self.unfollowings = []
        self.followed = []
        self.followerListFile = str(self.parent.enFollowerList.get())

        self.num_followerSt = int(self.parent.enFollowsSt.get())
        self.num_followerEd = int(self.parent.enFollowsEd.get())
        self.search_delaySt = int(self.parent.enSearchDelaySt.get())
        self.search_delayEd = int(self.parent.enSearchDelayEd.get())

        self.searchMethod = self.parent.cbSearchMethod.get()

        # Open Follower list file
        try:
            self.specified_file = open(self.followerListFile, "r")
            self.logger.error('Opened Follower List !')
        except:
            self.logger.error('Can not open ' + self.followerListFile + ' List !')
            return False
        return True
    def destory(self):
        self.specified_file.close()

    def start(self):
        self.num_followers = int(random.uniform(self.num_followerSt, self.num_followerEd))
        # self.moveHome()
        # return

        if self.controller.isBlueStack:
            self.controller.mouse_icon_double_click('icon')
            wait_start = int(self.actor.get_config('main', 'wait_start'))
            time.sleep(wait_start)

        # self.controller.scan('direct_scan')
        # return
        # self.controller.mouse_double_click_name('menu_search_search')
        # self.controller.ctrl_A()
        # self.followings.append('virat.kohli')
        # self.followings.append('webbly_r')
        # self.followings.append('celsoportiolli')

        if self.parent.doUnfollowing.get() == 1:
            self.checkFollowings()
            if self._stopevent.isSet():
                return
            self.removeUnfollowings()
            if self._stopevent.isSet():
                return
        else:
            self.logger.info('-> Discarded Unfollowing')

        # if not self.checkDate():
        #     return

        if self.searchMethod == "Through":
            if self.readAll == False:
                self.startNewFollowings_Through()
        elif self.searchMethod == "Direct":
            if self.readAll == False:
                self.startNewFollowings_Direct()
        elif self.searchMethod == "Random":
            self.startNewFollowings_Random()

        if self._stopevent.isSet():
            return

        if self.controller.isBlueStack:
            self.controller.close_icon_click('close')
            wait_end = int(self.actor.get_config('main', 'wait_end'))
            time.sleep(wait_end)

        # self.saveFollowingList()
        # if self._stopevent.isSet():
        #     return

    def moveHome(self):
        for x in range(5):
            time.sleep(1)
            if self.actor.backFromCancel():
                continue
            if self.actor.backFromBack():
                continue
            return
            

    def checkDate(self):
        d1 = datetime.now()
        d2 = datetime(2020, 4, 30)
        if d1 > d2:
            return False
        else :
            return True

    def loadNewFollowingList(self):
        self.logger.info('-> Loading Data')
        try:
            self.f = open(self.savedFilename, "r")
            for x in self.f:
                self.followings.append(x[:-1])
            self.f.close()
        except:
            pass
        finally:
            self.logger.info('<- Loading Data')

    def checkFollowings(self):
        if len(self.followings) == 0:
            self.logger.info('-> Nothing to Check Following')
            return

        self.logger.info('-> Check Following')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        time.sleep(1)
        self.controller.mouse_click_name('followers')
        time.sleep(4)

        self.unfollowings = []

        self.file_object = open(self.savedFollowers, 'a')
            # Append 'hello' at the end of file

        self.controller.mouse_double_click_name('search')
        time.sleep(1)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)

        for following in self.followings:
            if self._stopevent.isSet():
                break
            self.parent.setStatus(following + ' checking ...')
            self.controller.mouse_double_click_name('search')
            time.sleep(1)

            self.controller.key_input(following)
            self.waitSleep()

            [ret, follow_status] = self.actor.capture_search_result('item_follow')
            if ret and follow_status: # Keep
                self.followed.append(following)
                self.file_object.write(following + '\n')
                self.logger.critical('    ' + 'O ' + following)
                self.parent.setStatus(following + ' is following me')
            else : # remove
                self.unfollowings.append(following)
                self.logger.critical('    ' + 'X ' + following)
                self.parent.setStatus(following + ' is not following me')

            # self.controller.mouse_click_name('search')
            # self.controller.key_remove(following)
            self.controller.mouse_double_click_name('search_del')

        self.file_object.close()
        self.followings = []
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Check Following')

    def test(self):
        self.controller.mouse_click_name('home')
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

    def onlyUnfollow(self):
        self.num_followers = int(random.uniform(self.num_followerSt, self.num_followerEd))

        self.logger.info('-> Only Unfollowings')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')
        time.sleep(4)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)

        try:
            for i in range(self.num_followers):
                x = self.specified_file.readline()
                if not x:
                    self.logger.error('Tried all unfollowings!')
                    self.readAll = True
                    break
                unfollowing = x
                self.parent.setStatus(unfollowing + ' removing')

                if self._stopevent.isSet():
                    break
                self.controller.mouse_double_click_name('search')
                time.sleep(1)
                self.controller.key_input(unfollowing)

                self.waitSleep()

                [ret, follow_status] = self.actor.capture_search_result('item_follow')
                if ret and follow_status:
                    self.actor.unfollow_one(unfollowing)
                    self.logger.critical('    ' + '- ' + unfollowing)
                    self.parent.setStatus(unfollowing + ' removed')
                else:
                    self.followings.append(unfollowing)
                    self.logger.critical('    ' + '! ' + unfollowing)
                    self.parent.setStatus(unfollowing + ' not removed')

                # self.controller.mouse_click_name('search')
                # self.controller.key_remove(unfollowing)
                self.controller.mouse_double_click_name('search_del')
        except Exception as e:
            print('Error unfollowing one item', e)

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Remove Followings')

    def removeUnfollowings(self):
        if self._isPausedFollowing.isSet():
            return
        if len(self.unfollowings) == 0:
            self.logger.info('-> Nothing to Remove Following')
            return

        self.logger.info('-> Remove Followings')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')
        time.sleep(4)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)

        for unfollowing in self.unfollowings:
            if self._isPausedFollowing.isSet():
                return
            self.parent.setStatus(unfollowing + ' removing')

            if self._stopevent.isSet():
                break
            self.controller.mouse_double_click_name('search')
            time.sleep(1)
            self.controller.key_input(unfollowing)

            self.waitSleep()

            [ret, follow_status] = self.actor.capture_search_result('item_follow')
            if ret and follow_status:
                self.actor.unfollow_one(unfollowing)
                self.logger.critical('    ' + '- ' + unfollowing)
                self.parent.setStatus(unfollowing + ' removed')
            else:
                self.followings.append(unfollowing)
                self.logger.critical('    ' + '! ' + unfollowing)
                self.parent.setStatus(unfollowing + ' not removed')

            # self.controller.mouse_click_name('search')
            # self.controller.key_remove(unfollowing)
            self.controller.mouse_double_click_name('search_del')

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Remove Followings')

    def startNewFollowings_Through(self):
        if self._isPausedFollowing.isSet():
            return

        self.logger.info('-> Start Followings Through')
        self.controller.mouse_double_click_name('home')
        self.controller.mouse_double_click_name('menu_search')
        self.controller.mouse_double_click_name('menu_search_search')
        time.sleep(2)
        self.controller.mouse_double_click_name('menu_search_search')
        time.sleep(2)
        self.controller.key_input(str(self.parent.enFollower.get()))
        self.waitSleep()
        self.controller.mouse_click_name('search')
        self.waitSleep()
        self.controller.mouse_click_name('target_followers')
        self.controller.mouse_double_click_name('search')
        time.sleep(1)
        self.controller.mouse_double_click_name('search')
        time.sleep(1)
        if self._isPausedFollowing.isSet():
            return
        try:
            for i in range(self.num_followers):
                if self._isPausedFollowing.isSet():
                    break
                x = self.specified_file.readline()
                if not x:
                    self.logger.error('Tried all followings, Please wait until next check!')
                    self.readAll = True
                    break
                if self._stopevent.isSet():
                    break
                name = x[:-1]
                if name == '' or name == ' ':
                    continue
                self.parent.setStatus(name + ' - trying to follow')

                self.controller.mouse_double_click_name('search')
                time.sleep(1)
                self.controller.key_input(name)
                self.waitSleep()

                [ret, follow_status] = self.actor.capture_search_result('specified_follow')
                if not ret:
                    self.logger.info('    ' + 'N ' + name)
                    self.parent.setStatus(name + ' - Not found')
                elif follow_status:
                    self.logger.info('    ' + 'A ' + name)
                    self.parent.setStatus(name + ' - Already following')
                else:
                    self.controller.mouse_click_name('specified_follow')
                    time.sleep(1)
                    self.actor.remove_block()
                    self.followings.append(name)
                    self.logger.critical('    ' + '+ ' + name)
                    self.parent.setStatus(name + ' - new Following')

                self.controller.mouse_double_click_name('search_del')
                # self.controller.key_remove(name)
        except Exception as e:
            print('Error following one item', e)
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('search_cancel')
        self.controller.mouse_click_name('home')

        # name = self.controller.capture_text('item_name')
        # if name[0] == '#':
        #     return False
        self.logger.info('<- Start Followings Through')

    def startNewFollowings_Direct(self):
        if self._isPausedFollowing.isSet():
            return
        self.logger.info('-> Start Followings Direct')
        self.controller.mouse_double_click_name('home')
        self.controller.mouse_double_click_name('menu_search')
        self.controller.mouse_double_click_name('menu_search_search')
        if self._isPausedFollowing.isSet():
            return

        try:
            for i in range(self.num_followers):
                if self._isPausedFollowing.isSet():
                    break
                x = self.specified_file.readline()
                if not x:
                    self.logger.error('Tried all followings, Please wait until next check!')
                    self.readAll = True
                    break
                if self._stopevent.isSet():
                    break
                name = x[:-1]
                if name == '' or name == ' ':
                    continue
                self.parent.setStatus(name + ' - trying to follow')

                self.controller.mouse_double_click_name('menu_search_search')
                time.sleep(2)
                self.controller.key_input(str(name))
                self.waitSleep()
                # Check here if exists
                self.controller.mouse_click_name('search')
                self.waitSleep()
                # self.controller.mouse_click_name('posts')
                # self.controller.mouse_scroll_name('mid')
                # text = self.controller.capture_text('direct_follow')
                # print(text)
                # time.sleep(1)
                # if 'Follow' in text:
                #     self.controller.mouse_click_name('direct_follow')
                #     time.sleep(1)
                #     self.actor.remove_block()
                #     self.followings.append(name)
                #     self.logger.critical('    ' + '+ ' + name)
                #     self.parent.setStatus(name + ' - new Following')
                # else:
                #     self.logger.info('    ' + 'A ' + name)
                #     self.parent.setStatus(name + ' - Already following')

                scan_ret = self.controller.scan('direct_scan')
                time.sleep(1)
                if scan_ret:
                    self.actor.remove_block()
                    self.followings.append(name)
                    self.logger.critical('    ' + '+ ' + name)
                    self.parent.setStatus(name + ' - new Following')
                else:
                    self.logger.info('    ' + 'X ' + name)
                    self.parent.setStatus(name + ' - Not found or Already following')

                self.controller.mouse_click_name('back')

                # self.controller.mouse_double_click_name('menu_search_search')
                # self.controller.ctrl_A()
                # time.sleep(2)
                # self.controller.key_remove(name)
                self.controller.mouse_double_click_name('direct_del')
        except Exception as e:
            print('Error following one item', e)
        self.controller.mouse_click_name('search_cancel')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Start Followings Direct')

    def startNewFollowings_Random(self):
        self.logger.info('-> Start Followings Random')

        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        # self.controller.mouse_click_name('discover_suggested')
        self.controller.item_scroll_prepare()

        for i in range(self.num_followers):
            if self._stopevent.isSet():
                break
            self.controller.item_scroll_down()
            name = self.actor.follow_one()
            if name != '':
                self.followings.append(name)
                self.logger.critical('    ' + '+ ' + name)

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Start Followings Random')

    def saveFollowingList(self):
        self.logger.info('-> Save Data')
        with open(self.savedFilename, 'w+') as f:
            for name in self.followings:
                f.write(name + '\n')
        self.logger.info('<- Save Data')

    def waitSleep(self):
        value = random.uniform(self.search_delaySt, self.search_delayEd)
        self.parent.setStatus('Waiting for ' + str(int(value)) + ' seconds while loading ...')
        time.sleep(value)
        self.parent.setStatus('Working ...')
