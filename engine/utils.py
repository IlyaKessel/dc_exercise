import re
import logging

ORDERED_GROUPS = [1,3,5,7,9,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,
                  42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,
                  2,4,6,8,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,
                  63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99]


#https://www.ssa.gov/employer/ssns/HGJune2411_final.txt
#lates data for areas groups
GROUPS_FILE = 'highgroup.txt'

class SSNUtils:
    """
        SSN validation
        implemebation according to https://www.lexjansen.com/nesug/nesug07/ap/ap19.pdf 
    """
    AREA_TO_HIGHEST_RANK = None
    @classmethod
    def check_area_and_group(cls, area_number, group_number):
        """
            Checks validity of provided area and group
        """
        logging.debug(f'checking provided provided area and group')
        if cls.AREA_TO_HIGHEST_RANK is None:
            cls.__load_groups()
        group_rank = ORDERED_GROUPS[group_number - 1]
        curent_maximum_group_rank = cls.AREA_TO_HIGHEST_RANK[area_number]
        return group_rank < curent_maximum_group_rank
        
    @staticmethod
    def is_dummy_ssn(ssn_num_str: str):
        ssn_num = int(ssn_num_str.replace('-', ''))
        return ssn_num_str in ("078051120","111111111","123456789","219099999") or\
                (ssn_num >= 987654320 and ssn_num <= 987654329) or ssn_num == 999999999

    @classmethod
    def __load_groups(cls):
        if cls.AREA_TO_HIGHEST_RANK is None:
            with open(GROUPS_FILE) as groups_file:
                cls.AREA_TO_HIGHEST_RANK = {}
                for line in groups_file:
                    parts = line.strip().replace('*', ' ').split()
                    if parts and re.match(r'^\d{3}', parts[0]):
                        for i in range(0, len(parts), 2):
                            # related to 3 firsr digits
                            area_id = int(parts[i])
                            curent_highest_rank = ORDERED_GROUPS[int(parts[i + 1]) - 1]
                            cls.AREA_TO_HIGHEST_RANK[area_id] = curent_highest_rank