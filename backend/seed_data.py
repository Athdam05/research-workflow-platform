# seed_data.py
# Populates the database with realistic sample data for frontend development.
# Run with: python seed_data.py
# WARNING: Run this only once, or use --reset flag to wipe and re-seed.
#   python seed_data.py --reset

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db
from models.project_model import Project
from models.paper_model import Paper
from models.experiment_model import Experiment
from models.insight_model import Insight
from models.relationship_model import Relationship

app = create_app()

SAMPLE_DATA = [
    {
        "project": {
            "title": "Large Language Model Reasoning",
            "description": "Investigating chain-of-thought prompting and emergent reasoning in LLMs."
        },
        "papers": [
            {
                "title": "Chain-of-Thought Prompting Elicits Reasoning in LLMs",
                "link": "https://arxiv.org/abs/2201.11903",
                "tags": "LLM,reasoning,prompting,chain-of-thought",
                "summary": "Shows that prompting LLMs with intermediate reasoning steps dramatically improves performance on arithmetic, commonsense, and symbolic reasoning tasks.",
                "keywords": "chain-of-thought,few-shot,reasoning,arithmetic",
                "concepts": "emergent abilities,in-context learning,step-by-step reasoning"
            },
            {
                "title": "Self-Consistency Improves Chain of Thought Reasoning",
                "link": "https://arxiv.org/abs/2203.11171",
                "tags": "LLM,reasoning,self-consistency",
                "summary": "Proposes sampling diverse reasoning paths and marginalizing over them to improve CoT performance.",
                "keywords": "self-consistency,sampling,majority-vote",
                "concepts": "ensemble reasoning,output aggregation"
            }
        ],
        "experiments": [
            {
                "title": "CoT vs Standard Prompting on GSM8K",
                "hypothesis": "Chain-of-thought prompting will improve GPT-4 accuracy on GSM8K by more than 10%.",
                "method": "Evaluate GPT-4 on 500 random GSM8K samples with and without CoT. Measure exact-match accuracy.",
                "result": "CoT: 92% accuracy. Standard: 78% accuracy. Delta: +14%. Hypothesis confirmed."
            },
            {
                "title": "Self-Consistency with k=5 vs k=20 Samples",
                "hypothesis": "Increasing self-consistency samples from k=5 to k=20 yields diminishing returns.",
                "method": "Run self-consistency decoding with k in [1,5,10,20,40] on AQuA-RAT benchmark.",
                "result": "Accuracy plateau observed after k=10. k=20 shows only +0.8% over k=10. Hypothesis supported."
            }
        ],
        "insights": [
            "CoT benefits are strongly correlated with model size — models below 100B parameters show minimal gains.",
            "Self-consistency works best when the reasoning paths are diverse; temperature=0.7 outperforms greedy decoding.",
            "Arithmetic tasks benefit more from CoT than commonsense tasks, suggesting different reasoning pathways."
        ]
    },
    {
        "project": {
            "title": "Neural Architecture Search",
            "description": "Automating the design of neural network architectures using search algorithms."
        },
        "papers": [
            {
                "title": "Neural Architecture Search with Reinforcement Learning",
                "link": "https://arxiv.org/abs/1611.01578",
                "tags": "NAS,reinforcement-learning,architecture",
                "summary": "Uses an RNN controller trained with REINFORCE to generate and evaluate neural network architectures.",
                "keywords": "NAS,controller,REINFORCE,cell-search",
                "concepts": "automated ML,architecture optimization,search space"
            },
            {
                "title": "DARTS: Differentiable Architecture Search",
                "link": "https://arxiv.org/abs/1806.09055",
                "tags": "NAS,DARTS,differentiable",
                "summary": "Reformulates NAS as a differentiable problem by relaxing the discrete search space to continuous.",
                "keywords": "DARTS,bi-level optimization,continuous relaxation",
                "concepts": "gradient-based search,mixed operations,architecture weights"
            }
        ],
        "experiments": [
            {
                "title": "DARTS vs Random Search on CIFAR-10",
                "hypothesis": "DARTS will find a better architecture than random search within the same compute budget.",
                "method": "Run DARTS for 50 GPU hours and random search for 50 GPU hours on CIFAR-10. Compare top-1 accuracy.",
                "result": "DARTS: 97.1% top-1. Random search best: 96.4%. DARTS wins but margin is smaller than expected."
            }
        ],
        "insights": [
            "DARTS is sensitive to the search space definition — poorly chosen primitives lead to degenerate skip-connect architectures.",
            "Random search is a surprisingly strong baseline for NAS; DARTS advantage shrinks with larger search budgets."
        ]
    },
    {
        "project": {
            "title": "Multimodal Learning Research",
            "description": "Exploring joint learning across vision and language modalities."
        },
        "papers": [
            {
                "title": "CLIP: Learning Transferable Visual Models From Natural Language",
                "link": "https://arxiv.org/abs/2103.00020",
                "tags": "CLIP,vision-language,contrastive,zero-shot",
                "summary": "Trains vision-language models using contrastive learning on 400M image-text pairs, enabling zero-shot transfer.",
                "keywords": "contrastive learning,zero-shot transfer,image-text pairs",
                "concepts": "multimodal embeddings,shared representation space,zero-shot classification"
            }
        ],
        "experiments": [
            {
                "title": "CLIP Zero-Shot vs Linear Probe on ImageNet",
                "hypothesis": "CLIP zero-shot will match a linear probe trained on 10% of ImageNet.",
                "method": "Evaluate CLIP ViT-L/14 zero-shot on ImageNet val set. Train linear probe on 10%, 50%, 100% splits.",
                "result": "CLIP zero-shot: 75.3%. Linear probe 10%: 73.1%. 50%: 78.2%. Zero-shot beats 10% split — hypothesis confirmed."
            }
        ],
        "insights": [
            "CLIP's zero-shot ability degrades significantly on fine-grained datasets like Oxford Pets without prompt engineering.",
            "Prompt templates like 'a photo of a {label}' consistently outperform bare class name prompts by 3-5%."
        ]
    }
]


def seed():
    with app.app_context():
        print("\n🌱  Seeding database with sample data...\n")

        for data in SAMPLE_DATA:
            # Project
            project = Project(**data["project"])
            db.session.add(project)
            db.session.flush()  # get project.id before committing
            print(f"  📁  Project: {project.title}")

            # Papers
            paper_ids = []
            for p in data["papers"]:
                paper = Paper(project_id=project.id, **p)
                db.session.add(paper)
                db.session.flush()
                paper_ids.append(paper.id)
                print(f"       📄  Paper: {paper.title}")

            # Experiments (link to first paper)
            experiment_ids = []
            for i, e in enumerate(data["experiments"]):
                exp = Experiment(
                    project_id=project.id,
                    related_paper_id=paper_ids[0] if paper_ids else None,
                    **e
                )
                db.session.add(exp)
                db.session.flush()
                experiment_ids.append(exp.id)
                print(f"       🧪  Experiment: {exp.title}")

            # Insights (link to first paper + first experiment)
            insight_ids = []
            for content in data["insights"]:
                ins = Insight(
                    project_id=project.id,
                    content=content,
                    related_paper_id=paper_ids[0] if paper_ids else None,
                    related_experiment_id=experiment_ids[0] if experiment_ids else None,
                )
                db.session.add(ins)
                db.session.flush()
                insight_ids.append(ins.id)
                print(f"       💡  Insight: {content[:60]}...")

            # Relationships: paper → experiment → insight
            if paper_ids and experiment_ids:
                db.session.add(Relationship(
                    source_type="paper", source_id=paper_ids[0],
                    target_type="experiment", target_id=experiment_ids[0],
                    label="motivates"
                ))
            if experiment_ids and insight_ids:
                db.session.add(Relationship(
                    source_type="experiment", source_id=experiment_ids[0],
                    target_type="insight", target_id=insight_ids[0],
                    label="produces"
                ))
            if paper_ids and insight_ids:
                db.session.add(Relationship(
                    source_type="paper", source_id=paper_ids[0],
                    target_type="insight", target_id=insight_ids[0],
                    label="supports"
                ))

        db.session.commit()
        print(f"\n{'═'*50}")
        print(f"  ✅  Seeding complete!")
        print(f"  Projects:      {len(SAMPLE_DATA)}")
        print(f"  Papers:        {sum(len(d['papers']) for d in SAMPLE_DATA)}")
        print(f"  Experiments:   {sum(len(d['experiments']) for d in SAMPLE_DATA)}")
        print(f"  Insights:      {sum(len(d['insights']) for d in SAMPLE_DATA)}")
        print(f"  Relationships: {len(SAMPLE_DATA) * 3}")
        print(f"{'═'*50}\n")
        print("  Test it: http://127.0.0.1:5000/api/projects\n")


def reset():
    with app.app_context():
        print("\n🗑️   Resetting database...")
        db.drop_all()
        db.create_all()
        print("  ✅  All tables dropped and recreated.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true",
                        help="Wipe the database before seeding")
    args = parser.parse_args()

    if args.reset:
        reset()
    seed()
