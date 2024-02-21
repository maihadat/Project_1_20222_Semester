
class Sorter:
    def __init__(self, list_of_services):
        self.list_of_services = list_of_services
        self.training = {}
        self.support = {}
        self.typical = {}
        self.platform = {}
        self.info = {}
        self.reviews = {}
        self.service = {}

    def sort(self):
        _0 = 1
        _1 = 1
        _2 = 1
        _3 = 1
        _4 = 1
        _5 = 1
        tmp_dic = {}
        for service in self.list_of_services:
            if service.typical not in self.typical:
                self.typical[service.typical] = _1
                _1 += 1
            if service.support not in self.support:
                self.support[service.support] = _2
                _2 += 1
            if service.training not in self.training:
                self.training[service.training] = _3
                _3 += 1
            if service.platform not in self.platform:
                self.platform[service.platform] = _4
                _4 += 1
            tmp = [self.typical[service.typical], self.platform[service.platform], self.support[service.support], self.training[service.training]]
            tmp_str = ''.join([str(self.typical[service.typical]),  str(self.platform[service.platform]),
                               str(self.support[service.support]), str(self.training[service.training])])
            if tmp_str not in tmp_dic:
                tmp_dic[tmp_str] = _0
                self.info[_0] = tmp
                _0 += 1
            good_review = "\n".join(service.reviews[:3])
            bad_review = "\n".join(service.reviews[3:])
            self.reviews[_5] = [good_review, bad_review]
            self.service[_5] = [service.name, _5, tmp_dic[tmp_str], service.price, service.star, service.time, service.secure]
            _5 += 1






