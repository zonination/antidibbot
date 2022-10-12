# Import python libraries
import praw
import prawcore
import rlogin
import time
import re

# Log in to the bot
r=rlogin.ad()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Define initial conditions
hou = 1     # Number of hours to patiently wait until scolding user for flair
signature = '\n\n---\n\n^^This&nbsp;message&nbsp;automatically&nbsp;generated&nbsp;by&nbsp;a&nbsp;bot.&nbsp;Reply&nbsp;if&nbsp;you&nbsp;have&nbsp;any&nbsp;questions.'

# List blacklisted subreddits
blkPAR = ['funny', 'data_irl', 'me_irl', 'meirl', 'notinteresting', 'funnycharts', 'memes', 'TheLeftCantMeme']


# Module for checking inbox
def chkinbox():
    for message in r.inbox.unread(limit=10):
        try:
            # Skip non-messages and some accounts
            if not message.fullname.startswith("t4_") or message.author in ['mod_mailer', 'reddit', 'ModNewsletter']:
                message.mark_read()
                print('Marked as read: One of those annoying fucking Snoosletters.')
                continue
            # Skip non-subreddit messages
            if not message.subreddit:
                message.mark_read()
                print('Marked as read: non-subreddit message.')
                continue
        # Exception list for when Reddit inevitably screws up
        except praw.exceptions.APIException:
            print('  Probably a false alarm...')
        except (KeyboardInterrupt, SystemExit):
            raise


# Check for [D]ata [I]s [B]eautiful posts
def chkDIB():
    for post in r.subreddit('dataisugly').new(limit=10):
        try:
            cp = r.submission(str(post.crosspost_parent)[-6:])
            f = open('.log.txt', 'r')
            log = f.read().split(' ')
            f.close()
            if (cp.subreddit.display_name == 'dataisbeautiful') and (re.search('[\[\(][oO][cC][\]\)]', cp.title) is not None) and (post.id not in log):
                print('\n{0} invalid. (R3: OC from DiB)'.format(post.id))
                post.mod.remove(spam=False)
                print(' + Removed {0}'.format(post.id))
                post.mod.flair(text='R3: Dataisbeautiful', css_class='')
                print(' + Set Flair for {0}'.format(post.id))
                r.redditor(post.author.name).message(subject='Your submission was removed from /r/dataisugly', message='/u/{0}, thank you for your contribution. However, your submission was removed for the following reason(s):\n\n* 3\. This isn\'t the place to bitch about the latest OC in /r/dataisbeautiful. **(Non-OC by professionals is an exception).** You have the comments section of the /r/dataisbeautiful post for that, go there instead. This is not a space to mock the disabled.\n\nThis post has been removed. For information regarding this and similar issues please see the sidebar. If you have any questions, please feel free to [message the moderators.](https://www.reddit.com/message/compose?to=/r/dataisugly&subject=Question%20regarding%20the%20removal%20of%20this%20submission%20by%20%20{0}&message=I%20have%20a%20question%20regarding%20the%20removal%20of%20[this%20submission.](https://www.reddit.com{1}\))\n\n---\n\n[Link to your submission](https://www.reddit.com{1})'.format(post.author.name, post.permalink), from_subreddit='dataisugly')
                print(' + Messaged /u/{0}'.format(post.author.name))
                f = open('.log.txt', 'a+')
                f.write(' {0}'.format(post.id))
                print(' + Logged post ID: {0}'.format(post.id))
                for message in r.inbox.sent(limit=1):
                    f = open('.log.csv', 'a+')
                    f.write('\n{0},dataisbeautiful,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                    f.close()
                print(' + Added message to log file')
            elif cp.subreddit.display_name != 'dataisbeautiful':
                continue
                #print('  {0} OK. (Not /r/dataisbeautiful)'.format(post))
            elif (cp.subreddit.display_name == 'dataisbeautiful') and (re.search('[\[\(][oO][cC][\]\)]', cp.title) is None):
                continue
                #print('  {0} OK. (Non-OC from /r/dataisbeautiful)'.format(post))
            else:
                continue
                #print('  {0} OK. (Something else?)'.format(post))
            time.sleep(1)
        except AttributeError:
            continue
            #print('  {0} OK.'.format(post))

# Check for [PAR]ody subreddits
def chkPAR():
    for post in r.subreddit('dataisugly').new(limit=10):
        try:
            cp = r.submission(str(post.crosspost_parent)[-6:])
            f = open('.log.txt', 'r')
            log = f.read().split(' ')
            f.close()
            if (cp.subreddit.display_name in blkPAR) and (post.id not in log):
                print('\n{0} invalid. (R1: Intentional parody)'.format(post.id))
                post.mod.remove(spam=False)
                print(' + Removed {0}'.format(post.id))
                post.mod.flair(text='R1: Intentional Parody', css_class='')
                print(' + Set Flair for {0}'.format(post))
                r.redditor(post.author.name).message(subject='Your submission was removed from /r/dataisugly', message='/u/{0}, thank you for your contribution. However, your submission was removed for the following reason(s):\n\n* 1\. Please do not submit charts and graphics **intentionally drawn poorly for the sake of parody.** Go to /r/data_irl for that.\n\nThis post has been removed. For information regarding this and similar issues please see the sidebar. If you have any questions, please feel free to [message the moderators.](https://www.reddit.com/message/compose?to=/r/dataisugly&subject=Question%20regarding%20the%20removal%20of%20this%20submission%20by%20%20{0}&message=I%20have%20a%20question%20regarding%20the%20removal%20of%20[this%20submission.](https://www.reddit.com{1}\))\n\n---\n\n[Link to your submission](https://www.reddit.com{1})'.format(post.author.name, post.permalink), from_subreddit='dataisugly')
                # Log the post permanently
                print(' + Messaged /u/{0}'.format(post.author.name))
                f = open('.log.txt', 'a+')
                f.write(' {0}'.format(post.id))
                print(' + Logged post ID: {0}'.format(post.id))
                for message in r.inbox.sent(limit=1):
                    f = open('.log.csv', 'a+')
                    f.write('\n{0},parody,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                    f.close()
                print(' + Added message to log file')
            else:
                continue
                #print('  {0} OK. (not a joke/r/ sub)'.format(post))
            time.sleep(1)
        except AttributeError:
            continue
            #print('  {0} OK.'.format(post))


# Check for BRIGADING:
def chkBRIG():
    f = open('.log.txt', 'r')
    log = f.read().split(' ')
    f.close()
    for post in r.subreddit('dataisugly').new(limit=10):
        try:
            if (post.domain == 'reddit.com') and (post.id not in log) and (post.url.split('/')[3] != 'gallery'):
                print('\n{0} invalid (R4: Brigading)'.format(post.id))
                post.mod.remove(spam=False)
                print(' + Removed {0}'.format(post.id))
                post.mod.flair(text='R4: Brigading', css_class='')
                print(' + Set Flair for {0}'.format(post.id))
                r.redditor(post.author.name).message(subject='Your submission was removed from /r/dataisugly', message='/u/{0}, thank you for your contribution. However, your submission was removed for the following reason(s):\n\n* 4\. **Avoid brigading** of popular subreddits. It\'s against [Reddiquette](https://www.reddit.com/wiki/reddiquette) and could possibly get us in trouble. CROSSPOST GOOD. BRIGADING BAD.\n\nThis post has been removed. For information regarding this and similar issues please see the sidebar. If you have any questions, please feel free to [message the moderators.](https://www.reddit.com/message/compose?to=/r/dataisugly&subject=Question%20regarding%20the%20removal%20of%20this%20submission%20by%20%20{0}&message=I%20have%20a%20question%20regarding%20the%20removal%20of%20[this%20submission.](https://www.reddit.com{1}\))\n\n---\n\n[Link to your submission](https://www.reddit.com{1})'.format(post.author.name, post.permalink), from_subreddit='dataisugly')
                print(' + Messaged /u/{0}'.format(post.author.name))
                f = open('.log.txt', 'a+')
                f.write(' {0}'.format(post.id))
                print(' + Logged post ID: {0}'.format(post.id))
                # Log the message permanently
                for message in r.inbox.sent(limit=1):
                    f = open('.log.csv', 'a+')
                    f.write('\n{0},brigading,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                    f.close()
                print(' + Added message to log file')
        except IndexError:
            continue


# Check Flair Module
def chkflair():
    f = open('.log.txt', 'r')
    log = f.read().split(' ')
    f.close()
    f = open('.log2.txt', 'r')
    log2 = f.read().split(' ')
    f.close()
    for post in r.subreddit('dataisugly').new(limit=10):
        if (post.link_flair_text is None) and (post.id not in log) and ( ((time.time()-post.created_utc)/60)/60 > hou):
            print('\n{0} missing flair'.format(post.id))
            # Log the post, first and foremost
            f = open('.log.txt', 'a+')
            f.write(' {0}'.format(post.id))
            print(' + Logged post ID: {0}'.format(post.id))
            f.close()
            
            # Send a friendly reminder to flair the post 
            r.redditor(post.author.name).message(subject='A kind reminder to flair your post', message='Hey my dude /u/{0}, thank you for your contribution!\n\nI noticed [your post](https://old.reddit.com{1}) has been up for about [{2} hours](https://i.imgur.com/8VPMi9M.png), and the mods would like to send you a friendly reminder to [flair your post](https://i.imgur.com/4nhSwdd.png). Properly flaired posts help ensure the fun and mockery never stops! It also allows us to keep a searchable archive.\n\n[Here\'s a comprehensive guide](https://www.reddit.com/r/dataisugly/comments/fu8k69/lets_assign_ugly_flair/) in case you\'re new to this.\n\nCheers!{3}'.format(post.author.name, post.permalink, round((time.time() - post.created_utc)/60/60, 4), signature), from_subreddit='dataisugly')
            print(' + Sent a friendly reminder to /u/{0}'.format(post.author.name))
            post.report('Missing flair as of {0}'.format(time.asctime()))
            print(' + Sent a report to the mods')
            
            # Log the message permanently
            for message in r.inbox.sent(limit=1):
                f = open('.log.csv', 'a+')
                f.write('\n{0},no flair,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                f.close()
            print(' + Added to log file')

        elif (post.link_flair_text == 'Mostly OK') and (post.id not in log) and ( ((time.time()-post.created_utc)/60)/60 > hou):
            print('\n{0} using \'Mostly OK\' flair'.format(post.id))
            # Log the post, first and foremost
            f = open('.log.txt', 'a+')
            f.write(' {0}'.format(post.id))
            print(' + Logged post ID: {0}'.format(post.id))
            f.close()

            # Mostly OK? Send a friendly reminder to flair the post something else
            r.redditor(post.author.name).message(subject='Using "Mostly OK" Flair', message='Hey my dude /u/{0}, thank you for your contribution!\n\nI noticed [your post](https://old.reddit.com{1}) has been up for about [{2} hours](https://i.imgur.com/8VPMi9M.png). However, flairing with `Mostly OK` _this quickly_ is problematic. Here\'s a snippet from [the comprehensive guide](https://www.reddit.com/r/dataisugly/comments/fu8k69/lets_assign_ugly_flair/) in case you\'re new to this:\n\n>Are you willing to **admit defeat** at the hands of another redditor\'s proper and **civil** (be civil dammit) argument, but still think the graph is somewhat 50/50? **That\'s OK:** there\'s no shame in that. That\'s what makes you grow as an individual instead of being a stubborn heel digger.\n\n>Flair with this, **and the mods won\'t take it down for not admitting something wrong.**\n\n>(But it has to involve defeat at the hands of another redditor. You can\'t come barging in and immediately flair "Mostly OK" to claim  immunity, you doof.)\n\nChange your flair if you\'ve made a mistake, or reply to this if you\'ve _already_ gotten into a heated debate and it\'s an error on our end.{3}'.format(post.author.name, post.permalink, round((time.time() - post.created_utc)/60/60, 4), signature), from_subreddit='dataisugly')
            print(' + Sent a friendly reminder to /u/{0}'.format(post.author.name))
            post.report('MOSTLY OK flair on {0}'.format(time.asctime()))
            print(' + Sent a report to the mods')
            
            # Log the post, first and foremost
            f = open('.log.txt', 'a+')
            f.write(' {0}'.format(post.id))
            print(' + Logged post ID: {0}'.format(post.id))
            f.close()
            
            # Log the message permanently
            for message in r.inbox.sent(limit=1):
                f = open('.log.csv', 'a+')
                f.write('\n{0},OK flair,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                f.close()
            print(' + Added to log file')
                
        elif (post.link_flair_text == 'What the Fuck?') and (post.id not in log2) and ( ((time.time()-post.created_utc)/60)/60 + 1 > hou):
            print('\n{0} using \'WTF\' flair'.format(post.id))
            # Log the post, first and foremost
            f = open('.log2.txt', 'a+')
            f.write(' {0}'.format(post.id))
            print(' + Logged post ID: {0}'.format(post.id))
            f.close()
            
            # WTF? Message the mods:
            #r.redditor('post.author.name').message(subject='Using "WTF" flair.', message='Hey my dude /u/{0}.\n\nI noticed you were using `What the Fuck?` flair [for your post](https://old.reddit.com{1}). This is rarely used, so make _damn sure_ this is an instance [where it can be used](https://old.reddit.com/r/dataisugly/comments/fu8k69/lets_assign_ugly_flair/).\n\nChange your flair if you think you\'ve made a mistake to something better, or leave it alone if it best describes the situation.{2}'.format(post.author.name, post.permalink, signature))
            #print(' + Sent a message to the mods.'.format(post.author.name))
            
            # Report post
            post.report('WTF flair on {0}'.format(time.asctime()))
            print(' + Sent a report to the mods.')
            
            # Log the message permanently
            for message in r.inbox.sent(limit=1):
                f = open('.log.csv', 'a+')
                f.write('\n{0},WTF flair,https://www.reddit.com/message/messages/{1}'.format(post.author.name, message.id))
                f.close()
            print(' + Added to log file')

def archmail():
    #print('Checking modmail...')
    
    # Check all chains in inbox
    for chain in r.subreddit('dataisugly').modmail.conversations(limit=10, state='all'):
        
        # Keep and read a log of subreddit modmails, so we don't modmail twice.
        f = open('.mail.txt', 'r')
        log = f.read().split(' ')
        f.close()
        
        subjects = ['Your submission was removed from /r/dataisugly', 'Using "WTF" flair.', 'Using "Mostly OK" Flair', 'A kind reminder to flair your post']
        
        if (chain.subject in subjects) and (chain.id not in log):
            print(' + Modmail chain: {0}'.format(chain.id))
            
            # Count the number of replies
            n = 0
            for message in r.subreddit('dataisugly').modmail(chain.id, mark_read=True).messages:
                author = message.author.name
                n = n + 1
                
            if n == 1 and author == 'AntiDiBbot':
                
                # Caught a live one! Log the event
                f = open('.mail.txt', 'a+')
                log = f.write('{0} '.format(chain.id))
                f.close()
                
                print(' + Archiving chain.')
                chain.archive()
                
            elif n > 1:
                print(' + Another mod replied already: n = {0}\n'.format(n))
                # Log it anyway so we don't accidentally action it
                f = open('.mail.txt', 'a+')
                log = f.write('{0} '.format(chain.id))
            elif author != 'AntiDiBbot':
                # Log it anyway so we don't accidentally action it
                f = open('.mail.txt', 'a+')
                log = f.write('{0} '.format(chain.id))
                f.close()
            else:
                continue
            
        else:
            continue

# Main loop
while True:
    try:
        chkinbox()
        chkBRIG()
        chkDIB()
        chkPAR()
        chkflair()
        archmail()
        
        # Sleep for 5 minutes
        time.sleep(300)
    
    # Exception list for when Reddit inevitably screws up
    except praw.exceptions.APIException:
        print('\nAn API exception happened.\nTaking a coffee break.\n')
        time.sleep(30)
    except prawcore.exceptions.ServerError:
        print('\nReddit\'s famous 503 error occurred.\nTaking a coffee break.\n')
        time.sleep(180)
    except prawcore.exceptions.RequestException:
        print('.')
        time.sleep(180)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as inst:
        print(type(inst))
        print(inst.args)        
        print('')
        time.sleep(30)
#    except:
#        print('\nException happened (AntiDIBBot).\nTaking a coffee break.\n')
#        time.sleep(30)
