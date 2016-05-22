from django.db import models


class Comment(models.Model):
    content = models.TextField()
    _up_votes = models.IntegerField(default=0)
    _down_votes = models.IntegerField(default=0)
    _lower_bound = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    depth = models.PositiveIntegerField(default=0)
    path = models.TextField(null=True)
    parent = models.IntegerField(default=-1)

    @property
    def lower_bound(self):
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self):
        self.set_lower_bound()

    @property
    def up_votes(self):
        return self._up_votes

    @up_votes.setter
    def up_votes(self, value):
        self._up_votes += 1

    @property
    def down_votes(self):
        return self._down_votes

    @down_votes.setter
    def down_votes(self, value):
        self._down_votes += 1

    def set_lower_bound(self):
        n = self.up_votes + self.down_votes
        if n == 0:
            return 0
        pos = self.up_votes
        z = 1.96
        phat = 1.0*pos/n
        self.lower_bound = (phat + z*z/(2*n) - z *((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)**0.5

    def __unicode__(self):
        return 'Path: {0}, lb: {4}, depth: {5}, visible: {1}, up: {2}, down: {3}'.format(self.path, self.visible,
                                                                                         self.up_votes,
                                                                                         self.down_votes,
                                                                                         self.lower_bound, self.depth)