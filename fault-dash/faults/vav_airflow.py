from .profile import FaultProfile
from datadb import Data, find_runs, runs_longer_than
import pandas as pd
import os
import time

# hardcode data
raw_airflow = [{'2020-08-02T07:03:21+00:00': 444.89},
 {'2020-08-02T07:10:42+00:00': 442.22},
 {'2020-08-02T07:18:04+00:00': 442.09},
 {'2020-08-02T07:25:25+00:00': 445.42},
 {'2020-08-02T07:33:10+00:00': 446.75},
 {'2020-08-02T07:40:54+00:00': 443.43},
 {'2020-08-02T07:48:32+00:00': 442.22},
 {'2020-08-02T07:55:56+00:00': 440.61},
 {'2020-08-02T08:03:14+00:00': 441.82},
 {'2020-08-02T08:10:30+00:00': 443.56},
 {'2020-08-02T08:17:42+00:00': 446.49},
 {'2020-08-02T08:25:03+00:00': 445.29},
 {'2020-08-02T08:32:16+00:00': 446.49},
 {'2020-08-02T08:39:32+00:00': 444.89},
 {'2020-08-02T08:46:46+00:00': 444.36},
 {'2020-08-02T08:54:03+00:00': 445.95},
 {'2020-08-02T09:01:19+00:00': 446.62},
 {'2020-08-02T09:08:35+00:00': 443.16},
 {'2020-08-02T09:15:48+00:00': 448.21},
 {'2020-08-02T09:23:02+00:00': 446.88},
 {'2020-08-02T09:30:18+00:00': 445.69},
 {'2020-08-02T09:37:35+00:00': 441.69},
 {'2020-08-02T09:44:49+00:00': 442.22},
 {'2020-08-02T09:52:08+00:00': 437.51},
 {'2020-08-02T09:59:26+00:00': 440.08},
 {'2020-08-02T10:06:43+00:00': 442.36},
 {'2020-08-02T10:13:58+00:00': 442.89},
 {'2020-08-02T10:21:15+00:00': 418.71},
 {'2020-08-02T10:28:31+00:00': 455.15},
 {'2020-08-02T10:35:45+00:00': 386.36},
 {'2020-08-02T10:43:25+00:00': 456.97},
 {'2020-08-02T10:50:59+00:00': 415.02},
 {'2020-08-02T10:58:47+00:00': 440.35},
 {'2020-08-02T11:06:18+00:00': 461.35},
 {'2020-08-02T11:14:09+00:00': 453.59},
 {'2020-08-02T11:21:51+00:00': 457.61},
 {'2020-08-02T11:29:43+00:00': 452.67},
 {'2020-08-02T11:37:11+00:00': 444.89},
 {'2020-08-02T11:44:59+00:00': 459.81},
 {'2020-08-02T11:52:51+00:00': 439.54},
 {'2020-08-02T12:00:36+00:00': 449.79},
 {'2020-08-02T12:08:27+00:00': 466.45},
 {'2020-08-02T12:16:15+00:00': 459.16},
 {'2020-08-02T12:23:57+00:00': 450.05},
 {'2020-08-02T12:31:29+00:00': 457.49},
 {'2020-08-02T12:39:13+00:00': 365.74},
 {'2020-08-02T12:46:39+00:00': 439.27},
 {'2020-08-02T12:54:10+00:00': 442.22},
 {'2020-08-02T13:01:30+00:00': 438.05},
 {'2020-08-02T13:09:00+00:00': 418.85},
 {'2020-08-02T13:16:34+00:00': 478.98},
 {'2020-08-02T13:23:59+00:00': 445.02},
 {'2020-08-02T13:31:28+00:00': 445.02},
 {'2020-08-02T13:38:43+00:00': 419.42},
 {'2020-08-02T13:46:13+00:00': 452.02},
 {'2020-08-02T13:53:34+00:00': 460.97},
 {'2020-08-02T14:00:52+00:00': 452.15},
 {'2020-08-02T14:08:17+00:00': 454.37},
 {'2020-08-02T14:15:39+00:00': 420.54},
 {'2020-08-02T14:23:02+00:00': 438.59},
 {'2020-08-02T14:30:23+00:00': 444.63},
 {'2020-08-02T14:37:52+00:00': 459.16},
 {'2020-08-02T14:45:27+00:00': 439.4},
 {'2020-08-02T14:52:46+00:00': 445.69},
 {'2020-08-02T15:00:21+00:00': 440.21},
 {'2020-08-02T15:07:45+00:00': 452.54},
 {'2020-08-02T15:15:15+00:00': 442.49},
 {'2020-08-02T15:22:37+00:00': 449.66},
 {'2020-08-02T15:30:07+00:00': 450.31},
 {'2020-08-02T15:37:30+00:00': 461.86},
 {'2020-08-02T15:45:02+00:00': 445.02},
 {'2020-08-02T15:52:17+00:00': 452.67},
 {'2020-08-02T15:59:46+00:00': 805.65},
 {'2020-08-02T16:07:06+00:00': 797.45},
 {'2020-08-02T16:14:29+00:00': 790.67},
 {'2020-08-02T16:21:59+00:00': 792.61},
 {'2020-08-02T16:29:17+00:00': 806.46},
 {'2020-08-02T16:36:43+00:00': 703.69},
 {'2020-08-02T16:44:06+00:00': 804.77},
 {'2020-08-02T16:51:27+00:00': 805.13},
 {'2020-08-02T16:58:48+00:00': 786.54},
 {'2020-08-02T17:06:10+00:00': 800.56},
 {'2020-08-02T17:13:23+00:00': 802.34},
 {'2020-08-02T17:20:41+00:00': 795.97},
 {'2020-08-02T17:27:58+00:00': 791.79},
 {'2020-08-02T17:35:24+00:00': 790.44},
 {'2020-08-02T17:42:49+00:00': 797.75},
 {'2020-08-02T17:50:10+00:00': 795.74},
 {'2020-08-02T17:57:46+00:00': 605.0},
 {'2020-08-02T18:05:22+00:00': 426.97},
 {'2020-08-02T18:12:49+00:00': 453.33},
 {'2020-08-02T18:20:18+00:00': 461.86},
 {'2020-08-02T18:27:59+00:00': 453.33},
 {'2020-08-02T18:35:29+00:00': 455.41},
 {'2020-08-02T18:42:59+00:00': 440.61},
 {'2020-08-02T18:50:27+00:00': 440.61},
 {'2020-08-02T18:58:03+00:00': 453.33},
 {'2020-08-02T19:05:38+00:00': 449.52},
 {'2020-08-02T19:13:10+00:00': 453.98},
 {'2020-08-02T19:20:55+00:00': 452.02},
 {'2020-08-02T19:28:33+00:00': 455.93},
 {'2020-08-02T19:36:16+00:00': 450.31},
 {'2020-08-02T19:43:58+00:00': 452.8},
 {'2020-08-02T19:51:43+00:00': 451.36},
 {'2020-08-02T19:59:36+00:00': 453.46},
 {'2020-08-02T20:07:41+00:00': 452.02},
 {'2020-08-02T20:15:51+00:00': 453.59},
 {'2020-08-02T20:24:10+00:00': 453.98},
 {'2020-08-02T20:32:13+00:00': 455.02},
 {'2020-08-02T20:40:14+00:00': 454.37},
 {'2020-08-02T20:48:13+00:00': 450.18},
 {'2020-08-02T20:56:24+00:00': 455.41},
 {'2020-08-02T21:04:13+00:00': 795.82},
 {'2020-08-02T21:12:21+00:00': 788.19},
 {'2020-08-02T21:20:01+00:00': 798.34},
 {'2020-08-02T21:27:19+00:00': 801.6},
 {'2020-08-02T21:34:39+00:00': 792.61},
 {'2020-08-02T21:41:52+00:00': 791.87},
 {'2020-08-02T21:49:12+00:00': 800.86},
 {'2020-08-02T21:56:27+00:00': 802.04},
 {'2020-08-02T22:03:52+00:00': 795.67},
 {'2020-08-02T22:11:10+00:00': 795.22},
 {'2020-08-02T22:18:28+00:00': 774.1},
 {'2020-08-02T22:25:46+00:00': 789.09},
 {'2020-08-02T22:33:05+00:00': 786.99},
 {'2020-08-02T22:40:28+00:00': 801.82},
 {'2020-08-02T22:47:43+00:00': 787.22},
 {'2020-08-02T22:55:09+00:00': 803.81},
 {'2020-08-02T23:02:35+00:00': 446.49},
 {'2020-08-02T23:09:57+00:00': 453.07},
 {'2020-08-02T23:17:39+00:00': 440.08},
 {'2020-08-02T23:25:18+00:00': 449.39},
 {'2020-08-02T23:32:48+00:00': 437.38},
 {'2020-08-02T23:40:36+00:00': 450.97},
 {'2020-08-02T23:48:02+00:00': 452.28},
 {'2020-08-02T23:55:48+00:00': 444.36},
 {'2020-08-03T00:03:26+00:00': 445.29},
 {'2020-08-03T00:11:08+00:00': 460.19},
 {'2020-08-03T00:18:51+00:00': 445.69},
 {'2020-08-03T00:26:23+00:00': 443.03},
 {'2020-08-03T00:33:57+00:00': 452.15},
 {'2020-08-03T00:41:20+00:00': 445.95},
 {'2020-08-03T00:48:52+00:00': 464.29},
 {'2020-08-03T00:56:24+00:00': 445.95},
 {'2020-08-03T01:03:57+00:00': 446.75},
 {'2020-08-03T01:11:25+00:00': 438.32},
 {'2020-08-03T01:18:57+00:00': 453.59},
 {'2020-08-03T01:26:23+00:00': 442.09},
 {'2020-08-03T01:33:48+00:00': 439.4},
 {'2020-08-03T01:41:18+00:00': 446.09},
 {'2020-08-03T01:48:37+00:00': 443.16},
 {'2020-08-03T01:56:16+00:00': 435.48},
 {'2020-08-03T02:03:39+00:00': 444.23},
 {'2020-08-03T02:11:08+00:00': 455.67},
 {'2020-08-03T02:18:34+00:00': 448.07},
 {'2020-08-03T02:26:01+00:00': 451.89},
 {'2020-08-03T02:33:27+00:00': 449.92},
 {'2020-08-03T02:40:59+00:00': 455.41},
 {'2020-08-03T02:48:23+00:00': 450.84},
 {'2020-08-03T02:56:03+00:00': 455.15},
 {'2020-08-03T03:03:30+00:00': 805.28},
 {'2020-08-03T03:11:15+00:00': 794.18},
 {'2020-08-03T03:18:40+00:00': 799.97},
 {'2020-08-03T03:26:14+00:00': 796.34},
 {'2020-08-03T03:33:39+00:00': 797.15},
 {'2020-08-03T03:41:17+00:00': 794.25},
 {'2020-08-03T03:48:43+00:00': 802.41},
 {'2020-08-03T03:56:34+00:00': 792.99},
 {'2020-08-03T04:04:07+00:00': 796.26},
 {'2020-08-03T04:11:52+00:00': 833.31},
 {'2020-08-03T04:19:31+00:00': 797.53},
 {'2020-08-03T04:27:15+00:00': 814.78},
 {'2020-08-03T04:34:56+00:00': 791.94},
 {'2020-08-03T04:42:37+00:00': 766.72},
 {'2020-08-03T04:50:18+00:00': 785.94},
 {'2020-08-03T04:58:13+00:00': 436.02},
 {'2020-08-03T05:06:20+00:00': 457.36},
 {'2020-08-03T05:13:48+00:00': 448.34},
 {'2020-08-03T05:21:47+00:00': 457.36},
 {'2020-08-03T05:29:19+00:00': 451.76},
 {'2020-08-03T05:37:06+00:00': 452.15},
 {'2020-08-03T05:44:46+00:00': 438.32},
 {'2020-08-03T05:52:39+00:00': 445.95},
 {'2020-08-03T06:00:16+00:00': 443.43},
 {'2020-08-03T06:08:07+00:00': 459.16},
 {'2020-08-03T06:15:27+00:00': 447.02},
 {'2020-08-03T06:22:40+00:00': 445.16},
 {'2020-08-03T06:30:02+00:00': 454.5},
 {'2020-08-03T06:37:16+00:00': 457.61},
 {'2020-08-03T06:44:34+00:00': 456.45},
 {'2020-08-03T06:51:49+00:00': 459.42},
 {'2020-08-03T06:59:08+00:00': 468.1}]

raw_airflowsp = [{'2020-08-02T07:04:48+00:00': 450.0},
 {'2020-08-02T07:12:07+00:00': 450.0},
 {'2020-08-02T07:19:30+00:00': 450.0},
 {'2020-08-02T07:26:50+00:00': 450.0},
 {'2020-08-02T07:34:39+00:00': 450.0},
 {'2020-08-02T07:42:27+00:00': 450.0},
 {'2020-08-02T07:49:57+00:00': 450.0},
 {'2020-08-02T07:57:23+00:00': 450.0},
 {'2020-08-02T08:04:40+00:00': 450.0},
 {'2020-08-02T08:11:54+00:00': 450.0},
 {'2020-08-02T08:19:09+00:00': 450.0},
 {'2020-08-02T08:26:27+00:00': 450.0},
 {'2020-08-02T08:33:41+00:00': 450.0},
 {'2020-08-02T08:40:57+00:00': 450.0},
 {'2020-08-02T08:48:13+00:00': 450.0},
 {'2020-08-02T08:55:29+00:00': 450.0},
 {'2020-08-02T09:02:45+00:00': 450.0},
 {'2020-08-02T09:10:01+00:00': 450.0},
 {'2020-08-02T09:17:12+00:00': 450.0},
 {'2020-08-02T09:24:29+00:00': 450.0},
 {'2020-08-02T09:31:43+00:00': 450.0},
 {'2020-08-02T09:39:01+00:00': 450.0},
 {'2020-08-02T09:46:13+00:00': 450.0},
 {'2020-08-02T09:53:34+00:00': 450.0},
 {'2020-08-02T10:00:51+00:00': 450.0},
 {'2020-08-02T10:08:08+00:00': 450.0},
 {'2020-08-02T10:15:23+00:00': 450.0},
 {'2020-08-02T10:22:41+00:00': 450.0},
 {'2020-08-02T10:29:56+00:00': 450.0},
 {'2020-08-02T10:37:12+00:00': 450.0},
 {'2020-08-02T10:44:55+00:00': 450.0},
 {'2020-08-02T10:52:34+00:00': 450.0},
 {'2020-08-02T11:00:17+00:00': 450.0},
 {'2020-08-02T11:07:52+00:00': 450.0},
 {'2020-08-02T11:15:43+00:00': 450.0},
 {'2020-08-02T11:23:33+00:00': 450.0},
 {'2020-08-02T11:31:08+00:00': 450.0},
 {'2020-08-02T11:38:44+00:00': 450.0},
 {'2020-08-02T11:46:30+00:00': 450.0},
 {'2020-08-02T11:54:19+00:00': 450.0},
 {'2020-08-02T12:02:06+00:00': 450.0},
 {'2020-08-02T12:10:08+00:00': 450.0},
 {'2020-08-02T12:17:49+00:00': 450.0},
 {'2020-08-02T12:25:27+00:00': 450.0},
 {'2020-08-02T12:32:58+00:00': 450.0},
 {'2020-08-02T12:40:41+00:00': 450.0},
 {'2020-08-02T12:48:06+00:00': 450.0},
 {'2020-08-02T12:55:35+00:00': 450.0},
 {'2020-08-02T13:02:58+00:00': 450.0},
 {'2020-08-02T13:10:36+00:00': 450.0},
 {'2020-08-02T13:18:02+00:00': 450.0},
 {'2020-08-02T13:25:28+00:00': 450.0},
 {'2020-08-02T13:32:53+00:00': 450.0},
 {'2020-08-02T13:40:12+00:00': 450.0},
 {'2020-08-02T13:47:38+00:00': 450.0},
 {'2020-08-02T13:54:59+00:00': 450.0},
 {'2020-08-02T14:02:17+00:00': 450.0},
 {'2020-08-02T14:09:43+00:00': 450.0},
 {'2020-08-02T14:17:03+00:00': 450.0},
 {'2020-08-02T14:24:32+00:00': 450.0},
 {'2020-08-02T14:31:48+00:00': 450.0},
 {'2020-08-02T14:39:17+00:00': 450.0},
 {'2020-08-02T14:46:55+00:00': 450.0},
 {'2020-08-02T14:54:17+00:00': 450.0},
 {'2020-08-02T15:01:46+00:00': 450.0},
 {'2020-08-02T15:09:16+00:00': 450.0},
 {'2020-08-02T15:16:43+00:00': 450.0},
 {'2020-08-02T15:24:07+00:00': 450.0},
 {'2020-08-02T15:31:35+00:00': 450.0},
 {'2020-08-02T15:39:01+00:00': 450.0},
 {'2020-08-02T15:46:29+00:00': 450.0},
 {'2020-08-02T15:53:42+00:00': 450.0},
 {'2020-08-02T15:57:01+00:00': 790.0},
 {'2020-08-02T16:01:11+00:00': 790.0},
 {'2020-08-02T16:08:32+00:00': 790.0},
 {'2020-08-02T16:16:02+00:00': 790.0},
 {'2020-08-02T16:23:25+00:00': 790.0},
 {'2020-08-02T16:30:43+00:00': 790.0},
 {'2020-08-02T16:38:08+00:00': 790.0},
 {'2020-08-02T16:45:31+00:00': 790.0},
 {'2020-08-02T16:52:52+00:00': 790.0},
 {'2020-08-02T17:00:14+00:00': 790.0},
 {'2020-08-02T17:07:34+00:00': 790.0},
 {'2020-08-02T17:14:50+00:00': 790.0},
 {'2020-08-02T17:22:05+00:00': 790.0},
 {'2020-08-02T17:29:27+00:00': 790.0},
 {'2020-08-02T17:36:48+00:00': 790.0},
 {'2020-08-02T17:44:16+00:00': 790.0},
 {'2020-08-02T17:51:40+00:00': 790.0},
 {'2020-08-02T17:57:01+00:00': -1.0},
 {'2020-08-02T17:59:22+00:00': 450.0},
 {'2020-08-02T18:06:49+00:00': 450.0},
 {'2020-08-02T18:14:17+00:00': 450.0},
 {'2020-08-02T18:21:44+00:00': 450.0},
 {'2020-08-02T18:29:27+00:00': 450.0},
 {'2020-08-02T18:36:56+00:00': 450.0},
 {'2020-08-02T18:44:28+00:00': 450.0},
 {'2020-08-02T18:51:57+00:00': 450.0},
 {'2020-08-02T18:59:37+00:00': 450.0},
 {'2020-08-02T19:07:05+00:00': 450.0},
 {'2020-08-02T19:14:46+00:00': 450.0},
 {'2020-08-02T19:22:23+00:00': 450.0},
 {'2020-08-02T19:30:00+00:00': 450.0},
 {'2020-08-02T19:37:46+00:00': 450.0},
 {'2020-08-02T19:45:30+00:00': 450.0},
 {'2020-08-02T19:53:22+00:00': 450.0},
 {'2020-08-02T20:01:15+00:00': 450.0},
 {'2020-08-02T20:09:24+00:00': 450.0},
 {'2020-08-02T20:17:20+00:00': 450.0},
 {'2020-08-02T20:25:55+00:00': 450.0},
 {'2020-08-02T20:33:51+00:00': 450.0},
 {'2020-08-02T20:41:56+00:00': 450.0},
 {'2020-08-02T20:49:52+00:00': 450.0},
 {'2020-08-02T20:57:02+00:00': 790.0},
 {'2020-08-02T20:58:08+00:00': 790.0},
 {'2020-08-02T21:05:56+00:00': 790.0},
 {'2020-08-02T21:13:58+00:00': 790.0},
 {'2020-08-02T21:21:27+00:00': 790.0},
 {'2020-08-02T21:28:46+00:00': 790.0},
 {'2020-08-02T21:36:03+00:00': 790.0},
 {'2020-08-02T21:43:19+00:00': 790.0},
 {'2020-08-02T21:50:37+00:00': 790.0},
 {'2020-08-02T21:57:53+00:00': 790.0},
 {'2020-08-02T22:05:18+00:00': 790.0},
 {'2020-08-02T22:12:36+00:00': 790.0},
 {'2020-08-02T22:19:53+00:00': 790.0},
 {'2020-08-02T22:27:12+00:00': 790.0},
 {'2020-08-02T22:34:33+00:00': 790.0},
 {'2020-08-02T22:41:52+00:00': 790.0},
 {'2020-08-02T22:49:10+00:00': 790.0},
 {'2020-08-02T22:56:35+00:00': 790.0},
 {'2020-08-02T22:57:01+00:00': -1.0},
 {'2020-08-02T23:04:01+00:00': 450.0},
 {'2020-08-02T23:11:30+00:00': 450.0},
 {'2020-08-02T23:19:12+00:00': 450.0},
 {'2020-08-02T23:26:44+00:00': 450.0},
 {'2020-08-02T23:34:20+00:00': 450.0},
 {'2020-08-02T23:42:01+00:00': 450.0},
 {'2020-08-02T23:49:37+00:00': 450.0},
 {'2020-08-02T23:57:16+00:00': 450.0},
 {'2020-08-03T00:05:00+00:00': 450.0},
 {'2020-08-03T00:12:36+00:00': 450.0},
 {'2020-08-03T00:20:19+00:00': 450.0},
 {'2020-08-03T00:27:52+00:00': 450.0},
 {'2020-08-03T00:35:22+00:00': 450.0},
 {'2020-08-03T00:42:47+00:00': 450.0},
 {'2020-08-03T00:50:25+00:00': 450.0},
 {'2020-08-03T00:57:53+00:00': 450.0},
 {'2020-08-03T01:05:26+00:00': 450.0},
 {'2020-08-03T01:12:49+00:00': 450.0},
 {'2020-08-03T01:20:23+00:00': 450.0},
 {'2020-08-03T01:27:49+00:00': 450.0},
 {'2020-08-03T01:35:23+00:00': 450.0},
 {'2020-08-03T01:42:43+00:00': 450.0},
 {'2020-08-03T01:50:06+00:00': 450.0},
 {'2020-08-03T01:57:44+00:00': 450.0},
 {'2020-08-03T02:05:09+00:00': 450.0},
 {'2020-08-03T02:12:39+00:00': 450.0},
 {'2020-08-03T02:20:04+00:00': 450.0},
 {'2020-08-03T02:27:33+00:00': 450.0},
 {'2020-08-03T02:34:58+00:00': 450.0},
 {'2020-08-03T02:42:25+00:00': 450.0},
 {'2020-08-03T02:49:50+00:00': 450.0},
 {'2020-08-03T02:57:01+00:00': 790.0},
 {'2020-08-03T02:57:29+00:00': 790.0},
 {'2020-08-03T03:05:02+00:00': 790.0},
 {'2020-08-03T03:12:40+00:00': 790.0},
 {'2020-08-03T03:20:12+00:00': 790.0},
 {'2020-08-03T03:27:39+00:00': 790.0},
 {'2020-08-03T03:35:05+00:00': 790.0},
 {'2020-08-03T03:42:42+00:00': 790.0},
 {'2020-08-03T03:50:09+00:00': 790.0},
 {'2020-08-03T03:58:03+00:00': 790.0},
 {'2020-08-03T04:05:40+00:00': 790.0},
 {'2020-08-03T04:13:24+00:00': 790.0},
 {'2020-08-03T04:20:57+00:00': 790.0},
 {'2020-08-03T04:28:51+00:00': 790.0},
 {'2020-08-03T04:36:25+00:00': 790.0},
 {'2020-08-03T04:44:14+00:00': 790.0},
 {'2020-08-03T04:51:50+00:00': 790.0},
 {'2020-08-03T04:57:01+00:00': -1.0},
 {'2020-08-03T04:59:46+00:00': 450.0},
 {'2020-08-03T05:07:49+00:00': 450.0},
 {'2020-08-03T05:15:25+00:00': 450.0},
 {'2020-08-03T05:23:17+00:00': 450.0},
 {'2020-08-03T05:30:53+00:00': 450.0},
 {'2020-08-03T05:38:40+00:00': 450.0},
 {'2020-08-03T05:46:11+00:00': 450.0},
 {'2020-08-03T05:54:09+00:00': 450.0},
 {'2020-08-03T06:01:41+00:00': 450.0},
 {'2020-08-03T06:09:34+00:00': 450.0},
 {'2020-08-03T06:16:50+00:00': 450.0},
 {'2020-08-03T06:24:05+00:00': 450.0},
 {'2020-08-03T06:31:26+00:00': 450.0},
 {'2020-08-03T06:38:42+00:00': 450.0},
 {'2020-08-03T06:46:00+00:00': 450.0},
 {'2020-08-03T06:53:16+00:00': 450.0}]



class VAVAirflow(FaultProfile):
    def __init__(self): # TODO: the initialization should be updated as following also
        # TODO: Should be something exactly the same as in rogue_zone_temp.py as below
        # Commented because I can't test it locally


        # self.c = ReasonableClient("http://localhost:8000")
        # # self.c.load_file(f"../buildings/{building}/{model_name}.ttl")

        # tspsen = """SELECT ?sensor ?setpoint ?thing ?zone WHERE {
        #     ?sensor rdf:type brick:Temperature_Sensor .
        #     ?setpoint rdf:type brick:Temperature_Setpoint .
        #     ?sensor brick:isPointOf ?thing .
        #     ?setpoint brick:isPointOf ?thing .
        #     ?thing brick:controls?/brick:feeds+ ?zone .
        #     ?zone rdf:type brick:HVAC_Zone .
        #     FILTER NOT EXISTS { ?thing rdf:type brick:AHU }
        # }"""
        # self.tspsen = self.c.define_view('tspsen', tspsen)
        # doreload = not os.path.exists(f"{building}.db")
        # self.db = Data(f"../buildings/{building}", f"{building}.db",
        #                doreload=doreload)
        # self.grps = {}
        # tries = 5
        # while tries > 0:
        #     tries -= 1
        #     self.tspsen = self.tspsen.refresh()
        #     if len(self.tspsen) == 0:
        #         time.sleep(2)
        #         continue
        #     for (zone, grp) in self.tspsen.groupby('zone'):
        #         sps = grp.pop('setpoint')
        #         if len(sps.unique()) > 1:
        #             # use bounds
        #             hsps = self.db.filter_type2(self.c, sps, BRICK['Heating_Temperature_Setpoint'])
        #             csps = self.db.filter_type2(self.c, sps, BRICK['Cooling_Temperature_Setpoint'])
        #             if len(hsps) == 0 or len(csps) == 0:
        #                 continue
        #             grp.loc[:, 'hsp'] = hsps[0]
        #             grp.loc[:, 'csp'] = csps[0]
        #         elif len(sps.unique()) == 1:
        #             print(sps)
        #             grp.loc[:, 'hsp'] = sps.values[0]
        #             grp.loc[:, 'csp'] = sps.values[0]
        #         else:
        #             continue
        #         grp = grp.drop_duplicates()
        #         self.grps[zone] = grp
        #     break

        super().__init__("RogueZoneTemp")

    def get_fault_up_until(self, upperBound):
        faults = []

        #### formatting my data to dataframe ####
        airflow_data = pd.DataFrame({k:v for d in raw_airflow for k,v in d.items()}.items(), columns=['time', 'value'])
        airflow_data.set_index(['time'], inplace=True)
        airflow_data.index = pd.to_datetime(airflow_data.index,infer_datetime_format=True)
        vavsp_data = pd.DataFrame({k:v for d in raw_airflowsp for k,v in d.items()}.items(), columns=['time', 'value'])
        vavsp_data.set_index(['time'], inplace=True)
        vavsp_data.index = pd.to_datetime(vavsp_data.index, infer_datetime_format=True)
        #########################################
        # TODO: the above block should be replaced as in rogue_zone_temp.py below
        # sensor_data = self.db.data_before(upperBound, grp['sensor'])
        # hsp_data = self.db.data_before(upperBound, grp['hsp'])
        # csp_data = self.db.data_before(upperBound, grp['csp'])
        #########################################

        airflow_std = airflow_data.resample('1h').std()
        airflow_mean = airflow_data.resample('1h').mean()
        vavsp_data = vavsp_data.resample('1h').mean()

        df = pd.DataFrame()
        df['afstd'] = airflow_std['value']
        df['afmean'] = airflow_mean['value']
        df['vavsp'] = vavsp_data['value']

        zone_name = 'rm2109' # TODO: hardcode here

        duration_min = pd.to_timedelta('10T')
        constant_spots = list(find_runs(df, df['afstd'] < 5))
        if len(constant_spots) > 0:
            most_recent = constant_spots[-1]
            dur = most_recent[-1] - most_recent[0]
            dur = strfdelta(dur, "{hours} hours and {minutes} minutes")
            faults.append({
                'name': self.name,
                'key': f'constant-zone-{zone_name}', 
                'message': f"VAV constantly flowing for {dur}",
                'last_detected': most_recent[-1],
                'details': {
                    'Zone': zone_name
                }
            })

        overflow_spots = list(runs_longer_than(find_runs(df, df['afmean'] > df['vavsp']), duration_min))
        if len(constant_spots) > 0:
            most_recent = constant_spots[-1]
            dur = most_recent[-1] - most_recent[0]
            dur = strfdelta(dur, "{hours} hours and {minutes} minutes")
            faults.append({
                'name': self.name,
                'key': f'constant-zone-{zone_name}', 
                'message': f"VAV overflowing (airflow greater than setpoint) for {dur}",
                'last_detected': most_recent[-1],
                'details': {
                    'Zone': zone_name
                }
            })
        return faults


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)