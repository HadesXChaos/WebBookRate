<?php

namespace App\Console\Commands;

use App\Services\SearchService;
use Illuminate\Console\Command;

class IndexSearchCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'meilisearch:index';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Index all data into Meilisearch';

    /**
     * Execute the console command.
     */
    public function handle(SearchService $searchService): int
    {
        $this->info('Starting Meilisearch indexing...');

        try {
            $this->info('Indexing books...');
            $searchService->indexBooks();
            $this->info('Books indexed successfully.');

            $this->info('Indexing authors...');
            $searchService->indexAuthors();
            $this->info('Authors indexed successfully.');

            $this->info('Indexing reviews...');
            $searchService->indexReviews();
            $this->info('Reviews indexed successfully.');

            $this->newLine();
            $this->info('All data indexed successfully!');

            return Command::SUCCESS;
        } catch (\Exception $e) {
            $this->error('Error indexing data: ' . $e->getMessage());
            return Command::FAILURE;
        }
    }
}

