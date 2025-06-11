import consts
import json

event_sent_from_cust_msg = 'event_sent from customer '
event_rec_from_cust_msg = 'event_recv from customer '
event_sent_to_branch_msg = 'event_sent to branch '
event_rec_from_branch_msg = 'event_recv from branch '

def logfile(type, interface, event_id, logclock, obj_id, stub=None, tag=None):

    # global cust_out
    # global branch_out
    # global events_out

    event = {}
    event['id'] = obj_id
    event['customer-request-id'] = event_id
    event['logical_clock'] = logclock
    event['interface'] = interface
    event['type'] = type
    #event['comment'] = event_sent_msg + obj_id
    
    
    if type == 'customer':
        event['comment'] = event_sent_from_cust_msg + str(obj_id)
        # for objs in consts.cust_out:
        #     if objs['id'] == obj_id:
        #         objs['events'].append(event)
        #         consts.events_out.append(event)
        #         # print(events_out, cust_out)
        #         return
        # obj = {}
        # obj['id'] = obj_id
        # obj['type'] = type
        # obj['events'] = [event]
        # consts.events_out.append(event)
        # consts.cust_out.append(obj)
        # print(events_out, cust_out)
        with open(consts.OUTPUT_FILE_temp, 'a') as file:
            json.dump(event, file)
            file.write('\n')
    elif type == 'branch':
        # print("In branch ")
        if tag == 'R':
            if interface in ['query', 'deposit', 'withdraw']:
                # print("In branch 2")
                event['comment'] = event_rec_from_cust_msg + str(obj_id)
            elif interface in ['propogate_withdraw', 'propogate_deposit']:
                # print("In branch 3")
                # if stub:
                #     event['comment'] = event_sent_to_branch_msg + str(stub)
                # else:
                event['comment'] = event_rec_from_branch_msg + str(stub)
        if tag == 'S':
            event['comment'] = event_sent_to_branch_msg + str(stub)
        # print(event['comment'])
        # for objs in consts.branch_out:
        #     if objs['id'] == obj_id:
        #         objs['events'].append(event)
        #         print("bout", consts.branch_out)
        #         return
        # obj = {}
        # obj['id'] = obj_id
        # obj['type'] = type
        # obj['events'] = [event]
        # consts.events_out.append(event)
        # consts.branch_out.append(obj)
        # print("bout", branch_out)
        with open(consts.OUTPUT_FILE_temp, 'a') as file:
            json.dump(event, file)
            file.write('\n')
    
def writelog():
    # global cust_out
    # global branch_out
    # global events_out
    print("1", consts.branch_out)
    print("2", consts.cust_out)
    print("3", consts.events_out)
    # if type == 'cust': fname = consts.OUTPUT_FILE_customer
    # elif type == 'branch': fname = consts.OUTPUT_FILE_branch
    # elif type == 'events': fname = consts.OUTPUT_FILE_branch
    # with open(fname, 'a') as file:
    #     json.dump(output_obj, file)
    #     file.write('\n')

