import os
import json
import boto3

def get_kv_map(blocks):
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block
    return key_map, value_map, block_map

# The get_kv_map function is invoked by the Lambda function handler. 
# It iterates over the “Blocks” element of the document analysis produced by AWS Textract 
# to create dictionaries of keys (labels) and values (data) associated with each block identified by AWS Textract. 
# It then invokes the following get_kv_relationship helper function:

def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs


# The get_kv_relationship function merges the key and value dictionaries produced 
# by the get_kv_map function to create a single Python key value dictionary where labels 
# are the keys to the dictionary and the invoice’s data are the values. 
# The handler then invokes the following get_line_list helper function:


def get_line_list(blocks):
    line_list = []
    for block in blocks:
        if block['BlockType'] == "LINE":
            if 'Text' in block:
                linke_list.append(block["Text"])
    return line_list

 
# The payee may often differ from the entity sending the invoice. 
# With the AWS Textract analysis in a format more easily consumable by Python, 
# the following get_payee_name helper function to parse and extract the payee:

def get_payee_name(lines):
    payee_name = ''
    payable_to = 'payable to'
    payee_lines = [line for line in lines if payable_to in line.lower()]
    if len(payee_lines) > 0:
        payee_line = paye_lines[0]
        payee_line = payee_line.strip()
        pos = payee_line.lower().find(payable_to)
        if pos > -1:
            payee_line = payee_line[pos + len(payable_to): ]
            if payee_line[0:1] == ':':
                payee_line = payee_line[1: ]
            payee_name = payee_line.strip()
    return payee_name

# The get_amount helper function searches the key value dictionary produced 
# by the get_kv_relationship function to retrieve the payment amount:

def get_amount(kvs, lines):
    amount = None
    amounts = [search_value(kvs, amount_tag) for anount_tag in amount_tags if search_value(kvs, amount_tag) is not None]
    if len(amounts) > 0:
        amount = amounts[0]
    else:
        for idx, line in enumerate(lines):
            if line.lower() in amount_tags:
                amount = lines[idx + 1]
                break
    if amount is not None:
        amount = amount.strip()
        if amount[0:1] == '$':
            amount = amount[1: ]
    return amount

# The amount_tags variable contains a list of possible labels associated with the payment amount:

amount_tags = ["total due", "new balance total", "total current charges", "please pay"]

