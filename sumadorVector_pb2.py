# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: sumadorVector.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'sumadorVector.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13sumadorVector.proto\x12\rsumadorVector\" \n\rVectorRequest\x12\x0f\n\x07numeros\x18\x01 \x03(\x05\"!\n\x0cSumaResponse\x12\x11\n\tresultado\x18\x01 \x01(\x05\"%\n\x12SumaParcialRequest\x12\x0f\n\x07numeros\x18\x01 \x03(\x05\"*\n\x13SumaParcialResponse\x12\x13\n\x0bsumaParcial\x18\x01 \x01(\x05\"8\n\x10SumaFinalRequest\x12\x13\n\x0bsumaParcial\x18\x01 \x01(\x05\x12\x0f\n\x07numeros\x18\x02 \x03(\x05\x32Y\n\rCentroCalculo\x12H\n\x0bSumarVector\x12\x1c.sumadorVector.VectorRequest\x1a\x1b.sumadorVector.SumaResponse2b\n\tOperador1\x12U\n\x0cSumarParcial\x12!.sumadorVector.SumaParcialRequest\x1a\".sumadorVector.SumaParcialResponse2W\n\tOperador2\x12J\n\nSumarFinal\x12\x1f.sumadorVector.SumaFinalRequest\x1a\x1b.sumadorVector.SumaResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sumadorVector_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VECTORREQUEST']._serialized_start=38
  _globals['_VECTORREQUEST']._serialized_end=70
  _globals['_SUMARESPONSE']._serialized_start=72
  _globals['_SUMARESPONSE']._serialized_end=105
  _globals['_SUMAPARCIALREQUEST']._serialized_start=107
  _globals['_SUMAPARCIALREQUEST']._serialized_end=144
  _globals['_SUMAPARCIALRESPONSE']._serialized_start=146
  _globals['_SUMAPARCIALRESPONSE']._serialized_end=188
  _globals['_SUMAFINALREQUEST']._serialized_start=190
  _globals['_SUMAFINALREQUEST']._serialized_end=246
  _globals['_CENTROCALCULO']._serialized_start=248
  _globals['_CENTROCALCULO']._serialized_end=337
  _globals['_OPERADOR1']._serialized_start=339
  _globals['_OPERADOR1']._serialized_end=437
  _globals['_OPERADOR2']._serialized_start=439
  _globals['_OPERADOR2']._serialized_end=526
# @@protoc_insertion_point(module_scope)
