from img2dataset import download

if __name__ == "__main__":
    for i in range(10):
        output_dir = "vlm_captions_cc12m_%02d" % i
        download(
            processes_count=16,
            thread_count=32,
            url_list="./data/%s.parquet" % output_dir,
            image_size=None,
            resize_mode="no",
            output_folder=output_dir,
            output_format="files",
            input_format="parquet",
            url_col="url",
            caption_col="vlm_caption",
            enable_wandb=False,
            number_sample_per_shard=1000,
            distributor="multiprocessing",
        )
