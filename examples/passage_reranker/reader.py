from typing import Iterator

from texar.torch import HParams

from forte.common.resources import Resources
from forte.data.data_pack import DataPack
from forte.data.multi_pack import MultiPack
from forte.data.readers.base_reader import MultiPackReader
from ft.onto.base_ontology import Document


class EvalReader(MultiPackReader):

    # pylint: disable=no-self-use,unused-argument
    def _cache_key_function(self, collection) -> str:
        return "cached_string_file"

    # pylint: disable=attribute-defined-outside-init
    def initialize(self, resource: Resources, configs: HParams):
        self.resource = resource
        self.config = configs

    # pylint: disable=no-self-use
    def _collect(self, *args, **kwargs) -> Iterator[str]:
        file_path = args[0]
        with open(file_path, "r") as f:
            for line in f:
                yield line

    def _parse_pack(self, data_source: str) -> Iterator[MultiPack]:
        fields = data_source.split("\t")
        data_pack = DataPack(doc_id=fields[0])
        multi_pack = MultiPack()
        document = Document(pack=data_pack, begin=0, end=len(fields[1]))
        data_pack.add_entry(document)
        data_pack.set_text(fields[1])
        multi_pack.update_pack({self.config.pack_name: data_pack})
        yield multi_pack


class TrainReader(MultiPackReader):

    # pylint: disable=no-self-use,unused-argument
    def _cache_key_function(self, collection) -> str:
        return "cached_string_file"

    # pylint: disable=attribute-defined-outside-init
    def initialize(self, resource: Resources, configs: HParams):
        self.resource = resource
        self.config = configs

    # pylint: disable=no-self-use
    def _collect(self, *args, **kwargs) -> Iterator[str]:
        file_path = args[0]
        with open(file_path, "r") as f:
            for line in f:
                yield line

    def _parse_pack(self, data_source: str) -> Iterator[MultiPack]:
        fields = data_source.split("\t")
        multi_pack = MultiPack()
        query_pack = DataPack()
        document = Document(pack=query_pack, begin=0, end=len(fields[0]))
        query_pack.add_entry(document)
        query_pack.set_text(fields[0])
        multi_pack.update_pack({self.config.query_pack: query_pack})

        positive_passage = DataPack()
        document = Document(pack=positive_passage, begin=0, end=len(fields[1]))
        positive_passage.add_entry(document)
        positive_passage.set_text(fields[1])
        multi_pack.update_pack({self.config.positive_pack: positive_passage})

        negative_passage = DataPack()
        document = Document(pack=positive_passage, begin=0, end=len(fields[2]))
        negative_passage.add_entry(document)
        negative_passage.set_text(fields[1])
        multi_pack.update_pack({self.config.negative_pack: negative_passage})

        yield multi_pack
