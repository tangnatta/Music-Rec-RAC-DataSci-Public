# Music-Rec-RAC-DataSci
This project is the final project of RAC Data Science Camp (2023) with contributions of [**tangnatta**](https://github.com/tangnatta/) and [**IcyAlmondE**](https://github.com/IcyAlmondE/), published on IEEE Xplore at https://doi.org/10.1109/ICCI60780.2024.10532228.

## Setup
Please run `Set-ExecutionPolicy Unrestricted -Scope Process` in the powershell before running the script `.\music-rec-env\Scripts\Activate.ps1`.

```ps1
Set-ExecutionPolicy Unrestricted -Scope Process
.\music-rec-env\Scripts\Activate.ps1
```

## Introduction
Singing activities are becoming popular these days and many people sometimes reach the point that they don't know what to sing or don't know which songs are suitable for them. So the objective of this project is to make a recommendation system that can suggest songs that are suitable for the user's voice while also providing explaination to make them understand how to improve.

Why did we came up with this nearest neighbor thing? I can't really remember, but with the weighting of notes occurrences, it kinda worked pretty well.

## Methodology
The project is divided into 2 main parts: the song database creation and the recommendation. Here is the overview system of the project.

![スクリーンショット 2025-01-27 233833](https://github.com/user-attachments/assets/e07b4f67-c510-4699-9deb-8aedbb96ea2e)

In the song database creation part, we gathered around 100 songs in Thai, English, and Japanese and extracted only the vocal part using [Hybrid Demucs](https://github.com/facebookresearch/demucs). Then we sliced the singing audio of each song into 10ms intervals and converted each interval to notes using [CREPE](https://github.com/marl/crepe) while counting the occurrences of each note. The data was collected in a table with notes as binary and numeral occurrences of each note (See in the *Data Prep* folder).

In the recommendation part, we created an algorithm to find the similarity between user's singing data and songs in the database by converting the user's data to notes in each 10ms interval and using physics theory of music to calculate the singing score of each note. Then we used modified K-Nearest Neighbor, finding the Euclidean distance of the binary notes and weighting with the occurrences, to get the similarity score and rank them if the song is suitable for the user's singing voice.

We also designed a recommendation page showing the score of each note that the user can sing. The insight of each song is also available containing the number of notes in the song.

## Results
The system was tested by our friends and here's the results on the satisfaction of the recommendation and and the understanding of the explaination.

| Evaluation Criteria | Score |
| ------------------- | ----- |
| Satisfaction | 8.75 |
| Understanding | 7.05 |

## Conclusion
Future work may focus on refining the algorithm and exploring additional features for more vocal styles.
