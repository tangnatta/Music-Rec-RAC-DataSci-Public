import gradio as gr
import numpy as np
from pydub import AudioSegment
import librosa
import data_user
import knn
import data_music

df_musics = data_music.load_music_db()

LAST_RUN_KNN_RES = None
USER_DATA_RESULT = None
CURRENT_SONG = f"### Performance Analysis"


def analyze_voice(audio_path):
    global USER_DATA_RESULT, LAST_RUN_KNN_RES
# This is a simplified analysis - you would need to implement
# your own vocal analysis logic here
# try:
    user_data_result = data_user.user_data(audio_path)
    USER_DATA_RESULT = user_data_result
    # print(user_data_result)

    knn_res = knn.knn(df_musics, user_data_result)
    knn_res['score_fq'] = knn_res['score_fq'].map(lambda x: f"{x:.2f}")
    LAST_RUN_KNN_RES = knn_res

    recommendations = knn_res[['Name', 'score_fq']].sort_values(
        by='score_fq', ascending=False).head(10).values.tolist()

    performance_analysis = f"### Performance Analysis of {knn_res['Name'].iloc[0]}"

    # Simulate analysis scores (replace with actual analysis)

    overall_score, max_score, great_note_score, medium_note_score, need_improvement_score, min_score = knn.performace_analysis(
        knn_res, user_data_result, knn_res['Name'].iloc[0])

    # Format results
    results = {
        "Overall Score": f"{overall_score:.2f}%",
        "Max Score": f"{max_score:.2f}%",
        "Average Great Note Score": f"{great_note_score}%",
        "Average Medium Note Score": f"{medium_note_score}%",
        "Average Need Improvement Score": f"{need_improvement_score}%",
        "Min Score": f"{min_score:.2f}%",
        "Performance Analysis": performance_analysis
    }

    return results, recommendations
# except Exception as e:
#     print(e)
#     return str(e), []


# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# Song Recommendation System")
    gr.Markdown(
        "Recommender System for Singing-music according to Individual’s Vocal Abilities Using Modified K-Nearest Neighbor")
    gr.Markdown(
        "Upload your vocal performance to get detailed analysis and song recommendations")

    audio_input = gr.Audio(
        type="filepath",
        label="Upload Voice Recording (MP3)",
    )
    # Analyze button
    analyze_btn = gr.Button("Analyze Voice", variant="primary")
    with gr.Row():
        # with gr.Column():
        # Input

        # Output columns
        with gr.Column():
            # Song recommendations
            gr.Markdown("### Recommended Songs")
            recommendations = gr.Dataframe(
                headers=["Song", "Match Score"],
                type="array",
                label="Song Recommendations"
            )

        with gr.Column():
            # Performance metrics
            performance_analysis = gr.Markdown(
                f"### Performance Analysis")
            # gr.Markdown(f'Song: {song}')
            overall_score = gr.Label(label="Overall Score")
            max_score = gr.Label(label="Max Score")
            great_note = gr.Label(label="Average Great Note Score")
            medium_note = gr.Label(label="Average Medium Note Score")
            need_improvement = gr.Label(label="Average Need Improvement Score")
            min_score = gr.Label(label="Min Score")
            
        # gr.Markdown("### Explaination of Scores")
        

    # Handle the analysis
    def update_song_analysis(evt: gr.SelectData):
        global CURRENT_SONG

        current_song = LAST_RUN_KNN_RES['Name'].iloc[evt.index[0]]

        overall_score, max_score, great_note_score, medium_note_score, need_improvement_score, min_score = knn.performace_analysis(
            LAST_RUN_KNN_RES, USER_DATA_RESULT, current_song)

        # Return a list instead of dictionary
        return [
            f"{overall_score:.2f}%",
            f"{max_score:.2f}%",
            f"{great_note_score}%",
            f"{medium_note_score}%",
            f"{need_improvement_score}%",
            f"{min_score:.2f}%",
            f"### Performance Analysis of {current_song}"
        ]

    def update_outputs(audio):
        if audio is None:
            # Return a list instead of dictionary
            return [
                "No audio uploaded",
                "",
                "",
                "",
                "",
                "",
                [],
                "### Performance Analysis"
            ]

        # Save the audio file
        results, songs = analyze_voice(audio)

        # Return a list instead of dictionary
        return [
            results["Overall Score"],
            results["Max Score"],
            results["Average Great Note Score"],
            results["Average Medium Note Score"],
            results["Average Need Improvement Score"],
            results["Min Score"],
            songs,
            results["Performance Analysis"]
        ]

    analyze_btn.click(
        fn=update_outputs,
        inputs=[audio_input],
        outputs=[
            overall_score,
            max_score,
            great_note,
            medium_note,
            need_improvement,
            min_score,
            recommendations,
            performance_analysis
        ]
    )

    recommendations.select(
        fn=update_song_analysis,
        inputs=[],
        outputs=[
            overall_score,
            max_score,
            great_note,
            medium_note,
            need_improvement,
            min_score,
            performance_analysis
        ]
    )


if __name__ == "__main__":
    # Launch the app
    app.launch()
