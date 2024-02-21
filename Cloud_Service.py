

class CloudService:
    def __init__(self, id, name, info, price, reviews, star, time, secure=""):
        self.id = id
        self.name = name
        self.typical = info[0]
        self.platform = info[1]
        self.support = info[2]
        self.training = info[3]
        self.price = price
        self.reviews = reviews
        self.star = star
        self.time = time
        self.secure = secure

    def get_string(self):
        return 'Id: ' + str(self.id) + ', Name: ' + self.name + ', Star: ' + str(self.star)

    def less_than_star(self, CloudService):
        if self.star < CloudService.star:
            return True
        elif self.name < CloudService.name and self.star == CloudService.star:
            return True
        return False

    def less_than_name(self, CloudService):
        if self.name < CloudService.name:
            return True
        elif self.star < CloudService.star and self.name == CloudService.name:
            return True
        return False
    '''
    def __str__(self):
        return 'Id: ' + self.id + ', Name:' + self.name + ', Typical Customer: ' + self.typical + ', Platform: ' + self.platform + ', Price: ' + str(self.price) + ', Reviews: ' + str(self.reviews) + ', Star: ' + str(self.star)
    '''