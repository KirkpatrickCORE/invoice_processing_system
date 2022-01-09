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


def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs


def get_line_list(blocks):
    line_list = []
    for block in blocks:
        if block['BlockType'] == "LINE":
            if 'Text' in block:
                linke_list.append(block["Text"])
    return line_list


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



