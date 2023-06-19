# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: webhook.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rwebhook.proto\"M\n\nSubscriber\x12\x12\n\nblockchain\x18\x01 \x01(\t\x12\x16\n\x0ewallet_address\x18\x02 \x01(\t\x12\x13\n\x0bwebhook_url\x18\x03 \x01(\t\"\xf6\x01\n\x0bTransaction\x12\x12\n\nblockchain\x18\x01 \x01(\t\x12\x10\n\x08txn_hash\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x14\n\x0c\x62lock_number\x18\x04 \x01(\x05\x12\x11\n\ttimestamp\x18\x05 \x01(\x05\x12\x14\n\x0c\x61\x64\x64ress_from\x18\x06 \x01(\t\x12\x12\n\naddress_to\x18\x07 \x01(\t\x12\x0e\n\x06\x61mount\x18\x08 \x01(\x02\x12\x14\n\x0ctoken_symbol\x18\t \x01(\t\x12\x0f\n\x07\x64\x65\x63imal\x18\n \x01(\x05\x12\x18\n\x10\x63ontract_address\x18\x0b \x01(\t\x12\x0f\n\x07txn_fee\x18\x0c \x01(\x02\"\x07\n\x05\x45mpty\"]\n\x1aWebhookRegistrationRequest\x12\x12\n\nblockchain\x18\x01 \x01(\t\x12\x16\n\x0ewallet_address\x18\x02 \x01(\t\x12\x13\n\x0bwebhook_url\x18\x03 \x01(\t\",\n\x15WebhookInquireRequest\x12\x13\n\x0bwebhook_url\x18\x01 \x01(\t\"\xc0\x01\n\x18WebhookGetHistoryRequest\x12\x12\n\nblockchain\x18\x01 \x01(\t\x12\x16\n\x0ewallet_address\x18\x02 \x01(\t\x12\x18\n\x0bwebhook_url\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bstart_block\x18\x04 \x01(\x05H\x01\x88\x01\x01\x12\x16\n\tend_block\x18\x05 \x01(\x05H\x02\x88\x01\x01\x42\x0e\n\x0c_webhook_urlB\x0e\n\x0c_start_blockB\x0c\n\n_end_block\"`\n\x1bWebhookRegistrationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1f\n\nsubscriber\x18\x03 \x01(\x0b\x32\x0b.Subscriber\"\\\n\x16WebhookInquireResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12 \n\x0bsubscribers\x18\x03 \x03(\x0b\x32\x0b.Subscriber\"\x83\x01\n\x18WebhookDeleteAllResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12!\n\x19\x64\x65leted_subscribers_count\x18\x03 \x01(\x05\x12\"\n\x1a\x64\x65leted_transactions_count\x18\x04 \x01(\x05\"a\n\x19WebhookGetHistoryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\"\n\x0ctransactions\x18\x03 \x03(\x0b\x32\x0c.Transaction2\xd1\x02\n\x0eWebhookService\x12\x45\n\x08Register\x12\x1b.WebhookRegistrationRequest\x1a\x1c.WebhookRegistrationResponse\x12G\n\nUnregister\x12\x1b.WebhookRegistrationRequest\x1a\x1c.WebhookRegistrationResponse\x12:\n\x07Inquire\x12\x16.WebhookInquireRequest\x1a\x17.WebhookInquireResponse\x12.\n\tDeleteAll\x12\x06.Empty\x1a\x19.WebhookDeleteAllResponse\x12\x43\n\nGetHistory\x12\x19.WebhookGetHistoryRequest\x1a\x1a.WebhookGetHistoryResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'webhook_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SUBSCRIBER._serialized_start=17
  _SUBSCRIBER._serialized_end=94
  _TRANSACTION._serialized_start=97
  _TRANSACTION._serialized_end=343
  _EMPTY._serialized_start=345
  _EMPTY._serialized_end=352
  _WEBHOOKREGISTRATIONREQUEST._serialized_start=354
  _WEBHOOKREGISTRATIONREQUEST._serialized_end=447
  _WEBHOOKINQUIREREQUEST._serialized_start=449
  _WEBHOOKINQUIREREQUEST._serialized_end=493
  _WEBHOOKGETHISTORYREQUEST._serialized_start=496
  _WEBHOOKGETHISTORYREQUEST._serialized_end=688
  _WEBHOOKREGISTRATIONRESPONSE._serialized_start=690
  _WEBHOOKREGISTRATIONRESPONSE._serialized_end=786
  _WEBHOOKINQUIRERESPONSE._serialized_start=788
  _WEBHOOKINQUIRERESPONSE._serialized_end=880
  _WEBHOOKDELETEALLRESPONSE._serialized_start=883
  _WEBHOOKDELETEALLRESPONSE._serialized_end=1014
  _WEBHOOKGETHISTORYRESPONSE._serialized_start=1016
  _WEBHOOKGETHISTORYRESPONSE._serialized_end=1113
  _WEBHOOKSERVICE._serialized_start=1116
  _WEBHOOKSERVICE._serialized_end=1453
# @@protoc_insertion_point(module_scope)
