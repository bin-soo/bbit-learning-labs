#!/usr/bin/env python

# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from solution.consumer_sol import mqConsumer  # pylint: disable=import-error
import argparse
parser = argparse.ArgumentParser()

def main() -> None:
    parser.add_argument('-s', '--section')
    args = parser.parse_args()

    consumer = mqConsumer(binding_key=f"*.{args.section}.*",exchange_name=f"{args.section} Lab Exchange",queue_name=f"{args.section} Lab Queue")
    consumer.startConsuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
