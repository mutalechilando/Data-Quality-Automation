import json
import requests
from requests.auth import HTTPBasicAuth

# Replace with your credentials
username = 'admin'
password = 'district'

# Define the URL and payload
url = 'https://train.moh.gov.zm/lions/api/29/dataValueSets'
payload = {"dataValues":[
  {
    "dataElement": "fugax3aLtnS",
    "categoryOptionCombo": "qQFcogygYpT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "fugax3aLtnS",
    "categoryOptionCombo": "BCtpvb1gyEn",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "fugax3aLtnS",
    "categoryOptionCombo": "yuSVsObq1QQ",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 39
  },
  {
    "dataElement": "fugax3aLtnS",
    "categoryOptionCombo": "jSeiZPbdJqk",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 60
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "Etb79cTNmIK",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "ZjHIkuvbhVC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 24
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "GJ9gSSmJoIv",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 76
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "rj1w1Pq8jkf",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 109
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "C56tlhPFjfp",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 141
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "VZ2XN0ZxA6S",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 158
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "P02eYTPt4dS",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1602
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "uIpRFk3Jgz6",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 389
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "y01Z8E2MBYt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 998
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "Y4YXc8CkgNT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3922
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "WqDPWzWmlQT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 24
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "fzKC3XrqoHz",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 65
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "Ak2FdPn5Q9G",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 101
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "puTb3F0KdEX",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 241
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "Qqla7AHVmyE",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 678
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "u3zNA6CU0aC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2024
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "CTYuhOgISwV",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1552
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "oT9hPGqZ3pC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2035
  },
  {
    "dataElement": "xC1fdx2189O",
    "categoryOptionCombo": "zqBB8YN5eze",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 6790
  },
  {
    "dataElement": "RHUSiMw7L0U",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "RHUSiMw7L0U",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3
  },
  {
    "dataElement": "LuDfixmmeCS",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 11
  },
  {
    "dataElement": "LuDfixmmeCS",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 6
  },
  {
    "dataElement": "yJL1l2HGyfd",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 13
  },
  {
    "dataElement": "yJL1l2HGyfd",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 19
  },
  {
    "dataElement": "HKCdHdMoQKn",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 15
  },
  {
    "dataElement": "HKCdHdMoQKn",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 24
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "dWGZjkiAOVo",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "WxjqvDVB06u",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "Wilbot4TT1S",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "Ukae7tSpvKe",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "rSGvjpB7RBS",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 10
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "C8CEV5XYQ8A",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 5
  },
  {
    "dataElement": "Mdg8rn9wEe6",
    "categoryOptionCombo": "IWRJeiIvJdO",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 18
  },
  {
    "dataElement": "K62Ge7DVwsG",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "K62Ge7DVwsG",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "po7j7v40kTP",
    "categoryOptionCombo": "qayERYehMr0",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3
  },
  {
    "dataElement": "po7j7v40kTP",
    "categoryOptionCombo": "JbJ7CHM6Q4w",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 86
  },
  {
    "dataElement": "po7j7v40kTP",
    "categoryOptionCombo": "gd1YBlEs7og",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3238
  },
  {
    "dataElement": "rAIjw1a1eD4",
    "categoryOptionCombo": "dK7JQG4Lb9y",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 11
  },
  {
    "dataElement": "rAIjw1a1eD4",
    "categoryOptionCombo": "vwbokOFZ3g2",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 10
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "ZjHIkuvbhVC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "C56tlhPFjfp",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "VZ2XN0ZxA6S",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "P02eYTPt4dS",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "uIpRFk3Jgz6",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 12
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "y01Z8E2MBYt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 12
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "Y4YXc8CkgNT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 13
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "WqDPWzWmlQT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "Ak2FdPn5Q9G",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "puTb3F0KdEX",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 8
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "Qqla7AHVmyE",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 12
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "u3zNA6CU0aC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "CTYuhOgISwV",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 24
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "oT9hPGqZ3pC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 9
  },
  {
    "dataElement": "VYFMiXIdhIj",
    "categoryOptionCombo": "zqBB8YN5eze",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 20
  },
  {
    "dataElement": "V334esXWQEb",
    "categoryOptionCombo": "ZleizraaKrj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "V334esXWQEb",
    "categoryOptionCombo": "J6Nr6qFMo17",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 5
  },
  {
    "dataElement": "t3rO6WnzlnN",
    "categoryOptionCombo": "UHEIv6gqKnw",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 517
  },
  {
    "dataElement": "t3rO6WnzlnN",
    "categoryOptionCombo": "bU0ajXJsYN0",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1901
  },
  {
    "dataElement": "t3rO6WnzlnN",
    "categoryOptionCombo": "SihY6DoXso1",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 168
  },
  {
    "dataElement": "t3rO6WnzlnN",
    "categoryOptionCombo": "lRKjJul6NJ4",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "VZ2XN0ZxA6S",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "P02eYTPt4dS",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "uIpRFk3Jgz6",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 6
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "y01Z8E2MBYt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "cZx69LXFX3L",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 3
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "Y4YXc8CkgNT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 14
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "Ak2FdPn5Q9G",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "puTb3F0KdEX",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 7
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "Qqla7AHVmyE",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 21
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "u3zNA6CU0aC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 7
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "CTYuhOgISwV",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 28
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "oT9hPGqZ3pC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 13
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "RVUQtLjXQUJ",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "lQES6Ji9t7y",
    "categoryOptionCombo": "zqBB8YN5eze",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 20
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "GJ9gSSmJoIv",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 15
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "rj1w1Pq8jkf",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 12
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "C56tlhPFjfp",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 28
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "VZ2XN0ZxA6S",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 92
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "P02eYTPt4dS",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 28
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "uIpRFk3Jgz6",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 110
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "y01Z8E2MBYt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 81
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "KAguAK6wlor",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 8
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "cZx69LXFX3L",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 12
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "Y4YXc8CkgNT",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 102
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "fzKC3XrqoHz",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 20
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "Ak2FdPn5Q9G",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 14
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "puTb3F0KdEX",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 272
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "Qqla7AHVmyE",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 521
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "u3zNA6CU0aC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 20
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "CTYuhOgISwV",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 496
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "oT9hPGqZ3pC",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 325
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "qW2pqFeNu1X",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 7
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "RVUQtLjXQUJ",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 8
  },
  {
    "dataElement": "gKL94BRUewL",
    "categoryOptionCombo": "zqBB8YN5eze",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 247
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "U60jvtXJCf1",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 2
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "SYwkg6sSVc8",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 18
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "HDoJW6yt7mH",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 5
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "weIgm5FAqHp",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 13
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "egPA1OEtA0b",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "H1uPFmomoOt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 21
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "tMJKf4bl9Wq",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 19
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "eLgxzFysKFI",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 19
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "l4HWfzq6mf3",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1
  },
  {
    "dataElement": "gTZ1Ydlz8mH",
    "categoryOptionCombo": "Gki90Vi4iq0",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 37
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "U60jvtXJCf1",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 43
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "SYwkg6sSVc8",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 106
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "HDoJW6yt7mH",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 49
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "weIgm5FAqHp",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 151
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "egPA1OEtA0b",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "H1uPFmomoOt",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 321
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "tMJKf4bl9Wq",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 89
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "eLgxzFysKFI",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 60
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "l4HWfzq6mf3",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 218
  },
  {
    "dataElement": "AcFTT7zfwlx",
    "categoryOptionCombo": "Gki90Vi4iq0",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 1377
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "limuy4m5k2R",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "HW4QajJpbpV",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 30
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "qay1Msk8Cbh",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 36
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "IQlmNMHFTfM",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 30
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "Nudv35o5qnu",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 24
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "NPqNoR73Pbj",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 5
  },
  {
    "dataElement": "rt3nF4wbhGj",
    "categoryOptionCombo": "xMMqP2vjIme",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 7
  },
  {
    "dataElement": "PZtL9Ywkr0s",
    "categoryOptionCombo": "Vu2zii12O0P",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 132
  },
  {
    "dataElement": "M7Tbmz8G77Y",
    "categoryOptionCombo": "NNwNafbq7lJ",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 86
  },
  {
    "dataElement": "M7Tbmz8G77Y",
    "categoryOptionCombo": "K68JQnybhx0",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 50
  },
  {
    "dataElement": "xayGzfQJtQi",
    "categoryOptionCombo": "oqYcLgCW6ls",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 149
  },
  {
    "dataElement": "xayGzfQJtQi",
    "categoryOptionCombo": "VCTXUgeRuS6",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 4
  },
  {
    "dataElement": "xayGzfQJtQi",
    "categoryOptionCombo": "RN8CvGSMav7",
    "period": 202307,
    "orgUnit": "eCjzsmMZoAv",
    "value": 140
  }
 ]
 }

json_payload = json.dumps(payload)

# Set headers for JSON content
headers = {'Content-Type': 'application/json'}

# Authenticate with username and password
#auth = HTTPBasicAuth(username, password)

# Send the POST request
response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=json_payload)

# Print the response
print(response.status_code)
print(response.json())
