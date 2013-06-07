# -*- coding: utf-8 -*-
'''
Created on Sep 25, 2012

@author: moloch

    Copyright 2012 Root the Box

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
----------------------------------------------------------------------------

This file contains handlers related to the "Black Market" functionality

'''


from BaseHandlers import BaseHandler
from models import dbsession, MarketItem, Team

from libs.SecurityDecorators import authenticated


class MarketViewHandler(BaseHandler):
    ''' Renders views of items in the market '''

    @authenticated
    def get(self, *args, **kwargs):
        ''' Renders the main table '''
        user = self.get_current_user()
        self.render('market/view.html', user=user, errors=None)

    @authenticated
    def post(self, *args, **kwargs):
        ''' Called to purchase an item '''
        uuid = self.get_argument('uuid', '')
        item = MarketItem.by_uuid(uuid)
        if not item is None:
            user = self.get_current_user()
            team = Team.by_id(user.team.id)  # Refresh object
            if user.has_item(item.name):
                self.render('market/view.html',
                    user=user,
                    errors=["You have already purchased this item."]
                )
            elif team.money < item.price:
                message = "You only have $%d" % (team.money,)
                self.render('market/view.html', user=user, errors=[message])
            else:
                self.purchase_item(team, item)
                event = self.event_manager.create_purchased_item_event(user, item)
                self.new_events.append(event)
                self.redirect('/user/market')
        else:
            self.render('market/view.html',
                user=self.get_current_user(),
                errors=["Item does not exist."]
            )

    def purchase_item(self, team, item):
        ''' Conducts the actual purchase of an item '''
        team.money -= abs(item.price)
        team.items.append(item)
        dbsession.add(team)
        dbsession.flush()


class MarketDetailsHandler(BaseHandler):
    ''' Renders views of items in the market '''

    @authenticated
    def get(self, *args, **kwargs):
        ''' Get details on an item '''
        uuid = self.get_argument('uuid', '')
        item = MarketItem.by_uuid(uuid)
        if item is None:
            self.write({'Error': 'Item does not exist.'})
        else:
            self.write(item.to_dict())
        self.finish()
